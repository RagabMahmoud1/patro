from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.exceptions import UserError

from odoo.addons.account.wizard.pos_box import CashBox

class OrderLine(models.Model):
    _inherit='pos.order.line'
    qty_available = fields.Float(string="Quantity On Hand",compute='_calc_qty_available',store=True)
    return_qty = fields.Integer(string="Return Quantity", required=False)
    check_return_qty = fields.Boolean()
    discount_val = fields.Float(string="", compute="compute_discount_val")
    discount_fixed = fields.Float(string="Discount Fixed")
    commission = fields.Float(string='commission',compute='_calc_commission',store=True)
    @api.depends('product_id')
    def _calc_commission(self):
        for rec in self:
            if rec.product_id.commission:
                rec.commission=(rec.price_unit*(rec.product_id.commission/100))


    @api.onchange('discount_fixed')
    def onchange_discount_fixed(self):
        for rec in self:
            rec.discount = (rec.discount_fixed/(rec.qty * rec.price_unit) )* 100

    @api.onchange('discount')
    def onchange_discount22(self):
        for rec in self:
            rec.discount_fixed = (rec.qty * rec.price_unit) * rec.discount / 100

    @api.depends('discount')
    def compute_discount_val(self):
        for rec in self:
            rec.discount_val = (rec.qty * rec.price_unit) * rec.discount / 100

    @api.depends('product_id.qty_available')
    def _calc_qty_available(self):
       for line in self:
           line.qty_available=line.product_id.qty_available

    def _prepare_refund_data(self, refund_order, PosOrderLineLot):
        data=super(OrderLine,self)._prepare_refund_data(refund_order, PosOrderLineLot)
        data['return_qty']=self.qty
        print("D:::::::::::::::::::::::::::")
        data['check_return_qty']=True
        return data

    @api.constrains('qty', 'return_qty')
    def check_refund_qty(self):
        for line in self:
            print(":::::::::L", line.check_return_qty)
            if line.check_return_qty:
                if line.qty<0:
                    if abs(line.qty)>abs(line.return_qty):
                        raise ValidationError("Refunded Qty Greater Than Order Qtuantity")








class Order(models.Model):
    _inherit='pos.order'
    sales_person = fields.Many2one(comodel_name='res.users',string="Sales Person")
    def _order_fields(self, ui_order):
        order = super(Order, self)._order_fields(ui_order)
        order['sales_person'] = ui_order.get('sales_person')
        return order


    def _prepare_refund_values(self, current_session):
        data = super(Order, self)._prepare_refund_values(current_session)
        data['sales_person']=self.sales_person.id
        return data

    def _export_for_ui(self, order):
        for rec in self:
            data = super(Order, rec)._export_for_ui(order)
            data['sales_person'] = rec.sales_person.id
        return data



    def get_return_days(self):
        with_user = self.env['ir.config_parameter'].sudo()
        return_days = int(with_user.get_param('project_custom.return_days')) or 14
        return return_days

    debit = fields.Monetary(default=0.0,related='partner_id.debit',store=True )
    credit = fields.Monetary(default=0.0,related='partner_id.credit',store=True )
    return_days = fields.Integer(string="Return Days", required=False, default=lambda self:self.get_return_days())



    def refund(self):
        res=super(Order,self).refund()
        for order in self:
            days=(datetime.now().date()-order.date_order.date()).days
            return_days = order.return_days or 14
            if days>=return_days:
                raise ValidationError("انتهت صلاحية استرجاع الفاتورة!")
        return res


class PosConfig(models.Model):
    _inherit='pos.config'
    return_days = fields.Integer(string="Return Days",compute='_calc_return_days')

    def get_return_days(self):
        with_user = self.env['ir.config_parameter'].sudo()
        return_days = int(with_user.get_param('project_custom.return_days')) or 14
        return return_days
    def _calc_return_days(self):
        for con in self:
            con.return_days=self.get_return_days()
class Session(models.Model):
    _inherit='pos.session'

    def try_cash_in_out(self, _type, amount, reason, extras):
        print("extras",extras)
        sign = 1 if _type == 'in' else -1
        if 'item_id' in extras.keys():
            self.env['cash.box.out']\
                .with_context({'active_model': 'pos.session', 'active_ids': self.ids})\
                .create({'amount': sign * amount, 'name': reason,'item_id':int(extras.get('item_id')) or False})\
                .run()
        else:
            self.env['cash.box.out'] \
                .with_context({'active_model': 'pos.session', 'active_ids': self.ids}) \
                .create(
                {'amount': sign * amount, 'name': reason}) \
                .run()
        message_content = [f"Cash {extras['translatedType']}", f'- Amount: {extras["formattedAmount"]}']
        if reason:
            message_content.append(f'- Reason: {reason}')
        self.message_post(body='<br/>\n'.join(message_content))

class PosBox(CashBox):
    _register = False
    item_id = fields.Many2one(comodel_name="cash.items", string="بند", required=False)



class PosBoxOut(PosBox):
    _inherit = 'cash.box.out'

    def _calculate_values_for_statement_line(self, record):
        values = super(PosBoxOut, self)._calculate_values_for_statement_line(record)
        active_model = self.env.context.get('active_model', False)
        active_ids = self.env.context.get('active_ids', [])
        if active_model == 'pos.session' and active_ids:
            values['ref'] = self.env[active_model].browse(active_ids)[0].name
        values['item_id']=self.item_id.id
        return values

class PosOrderReport(models.Model):
    _inherit = "report.pos.order"
    sales_person = fields.Many2one(comodel_name='res.users',string="Sales Person")


    ore_id = fields.Many2one(comodel_name="product.ore", string="نوع الخامة", required=False)
    session_id2 = fields.Many2one(comodel_name="product.session", string="الموسم", required=False)
    model_year = fields.Char(string='Model Year', required=False)
    color = fields.Char(string='Color')
    size = fields.Char(string='Size')
    commission = fields.Float(string='commission')

    def _select(self):
        return super(PosOrderReport, self)._select() + ',pt.session_id AS session_id2,' \
                                                       'pt.ore_id AS ore_id,' \
                                                       'p.color AS color,' \
                                                       'p.size AS size,' \
                                                       's.sales_person AS sales_person,' \
                                                       'l.commission AS commission,' \
                                                       'pt.model_year AS model_year'

    def _group_by(self):
        return super(PosOrderReport, self)._group_by() + ',pt.session_id,pt.ore_id,pt.model_year,p.color,p.size,l.commission,s.sales_person'\



