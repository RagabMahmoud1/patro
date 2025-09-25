# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from collections import defaultdict


class A(models.Model):
    _inherit='product.attribute'
    is_color = fields.Boolean(string='Is Color')
    is_size = fields.Boolean(string='Is Size')



class ProductOre(models.Model):
    _name='product.ore'
    name = fields.Char(string="Name", required=True)

class ProductSession(models.Model):
    _name='product.session'
    name = fields.Char(string="Name", required=True)
    cost_percentage = fields.Float(string="Cost Percentage", required=False)
    cost = fields.Float(string="Cost", required=False)

class ProductTemplate(models.Model):
    _inherit='product.template'
    ore_id = fields.Many2one(comodel_name="product.ore", string="نوع الخامة", required=False)
    session_id = fields.Many2one(comodel_name="product.session", string="الموسم", required=False)
    manual_barcode = fields.Boolean(string="Manual Barcode Generator")
    cost_percentage = fields.Float(string="Cost Percentage",compute='_calc_cost_percentage',store=True,readonly=False)
    model_year = fields.Char(string='Model Year', required=False)
    vendors = fields.Many2many(comodel_name='res.partner',compute='_calc_vendors',store=True)
    commission = fields.Float(
        string='commission',
        required=False)

    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):

        if args is None:
            args = []
        search_domain = ['|', ('barcode', operator, name), '|', ('default_code', operator, name),
                         ('name', operator, name)]
        return list(self._search(search_domain + args, limit=limit))

   # def name_get(self):

    #    res = []
     #   disp = ''
      #  for rec in self:
       #     disp = str(rec.name) + str(rec.default_code)
        #    res.append((rec.id, disp))
       # return res

    @api.depends('seller_ids')
    def _calc_vendors(self):
        for rec in self:
            rec.vendors=[(6, 0, [x.id for x in rec.seller_ids.mapped('name')])]

    @api.onchange('cost_percentage')
    def onchange_cost_percentage(self):
        self.standard_price = self.list_price * (self.cost_percentage / 100)

    @api.depends('session_id.cost_percentage','session_id.cost','categ_id.cost_percentage')
    def _calc_cost_percentage(self):
      for prod in self:
          if prod.session_id:
            if prod.session_id.cost_percentage:
                prod.cost_percentage=prod.session_id.cost_percentage
                prod.standard_price = prod.list_price * (prod.cost_percentage / 100)
            if prod.session_id.cost:
                prod.standard_price=prod.session_id.cost
          elif prod.categ_id.cost_percentage:
              prod.cost_percentage=prod.categ_id.cost_percentage
              prod.standard_price = prod.list_price * (prod.cost_percentage / 100)


    @api.constrains('name')
    def check_name(self):
        if self.name:
            if len(self.env['product.template'].search([("name", "=", self.name)])) > 1:
                raise ValidationError("Product Name already exists")



    @api.model
    def create(self, values):
        if values.get('barcode') and values.get('manual_barcode') == False:
            values['barcode'] = ''
        res = super(ProductTemplate, self).create(values)
        if res.manual_barcode==False:
            res.barcode = str(res.id)+"-H"
        return res

    def write(self, values):
        if values.get('barcode') and values.get('manual_barcode') == False:
            values['barcode'] = self.id
        res = super(ProductTemplate, self).write(values)
        return res

    @api.constrains('barcode')
    def check_barcode(self):
        if self.barcode:
            if len(self.env['product.template'].search([("barcode", "=", self.barcode)])) > 1:
                raise ValidationError("Barcode already exists")


class Product(models.Model):
    _inherit='product.product'
    cost_percentage = fields.Float(string="Cost Percentage", compute='_calc_cost_percentage', store=False,
                                   readonly=False)
    color = fields.Char(string='Color',compute='_calc_color',store=True)
    size = fields.Char(string='Size',compute='_calc_color',store=True)

    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):

        if args is None:
            args = []
        search_domain = ['|', ('barcode', operator, name), '|', ('default_code', operator, name),
                         ('name', operator, name)]
        return list(self._search(search_domain + args, limit=limit))

    #def name_get(self):

     #   res = []
      #  disp = ''
       # for rec in self:
        #    disp = str(rec.name) + str(rec.default_code)
         #   res.append((rec.id, disp))
       # return res

    @api.depends('product_template_variant_value_ids','product_template_variant_value_ids.attribute_id.is_color','product_template_variant_value_ids.attribute_id.is_size')
    def _calc_color(self):
        for rec in self:
            for value in rec.product_template_variant_value_ids:
                if value.product_attribute_value_id.attribute_id.is_color:
                   rec.color= value.product_attribute_value_id.name
                if value.product_attribute_value_id.attribute_id.is_size:
                    rec.size = value.product_attribute_value_id.name


    @api.onchange('cost_percentage')
    def onchange_cost_percentage(self):
        self.standard_price = self.list_price * (self.cost_percentage / 100)

    @api.depends('session_id.cost_percentage', 'session_id.cost', 'categ_id.cost_percentage')
    def _calc_cost_percentage(self):
        for prod in self:
            if prod.session_id:
                if prod.session_id.cost_percentage:
                    prod.cost_percentage = prod.session_id.cost_percentage
                    prod.standard_price = prod.list_price * (prod.cost_percentage / 100)
                if prod.session_id.cost:
                    prod.standard_price = prod.session_id.cost
            elif prod.categ_id.cost_percentage:
                prod.cost_percentage = prod.categ_id.cost_percentage
                prod.standard_price = prod.list_price * (prod.cost_percentage / 100)

   
    @api.model
    def create(self, values):
        if values.get('barcode') and values.get('manual_barcode')==False:
            values['barcode']=''
        res=super(Product ,self).create(values)
        if res.manual_barcode == False:
            res.barcode = str(res.product_tmpl_id.id)+str(res.id)+"-H"
        return res

    def write(self, values):
        if values.get('barcode') and values.get('manual_barcode')==False:
            values['barcode'] =str(self.product_tmpl_id.id)+str(self.id)+"-H"
        res=super(Product, self).write(values)
        return res

    @api.constrains('barcode')
    def check_barcode(self):
        if self.barcode:
            if len(self.env['product.product'].search([("barcode", "=", self.barcode)])) > 1:
                raise ValidationError("Barcode already exists")

    barcode2 = fields.Char(string="Gernal Barcode", compute='_calc_barcode', search='_search_barcode', store=False)

    @api.depends('barcode')
    def _calc_barcode(self):
        for rec in self:
            rec.barcode2 = rec.barcode

    def _search_barcode(self, operator, value):
        print("D>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
        product_temp = self.env['product.product'].search([('barcode', '=', value)], limit=1)
        if product_temp:
            return [('product_tmpl_id', '=', product_temp.product_tmpl_id.id)]
        else:
            return []


class Partner(models.Model):
    _inherit='res.partner'
    total_due = fields.Monetary()
    @api.constrains('name')
    def check_name(self):
        if self.name:
            if len(self.env['res.partner'].search([("name", "=", self.name)])) > 1:
                raise ValidationError("Partner Name already exists")

    @api.model
    def create_from_ui(self, partner):
        """ create or modify a partner from the point of sale ui.
            partner contains the partner's fields. """
        # image is a dataurl, get the data after the comma
        if not partner.get('phone'):
            raise ValidationError(_("You Must Add Phone"))
        if partner.get('image_1920'):
            partner['image_1920'] = partner['image_1920'].split(',')[1]
        partner_id = partner.pop('id', False)
        if partner_id:  # Modifying existing partner
            self.browse(partner_id).write(partner)
        else:
            partner_id = self.create(partner).id
        return partner_id


"""
class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'



    def _prepare_report_data(self):
        # if self.custom_quantity <= 0:
        #     raise UserError(_('You need to set a positive quantity.'))
        # Get layout grid
        if self.print_format == 'dymo':
            xml_id = 'product.report_product_template_label_dymo'
        elif 'x' in self.print_format:
            xml_id = 'product.report_product_template_label'
        else:
            xml_id = ''

        active_model = ''
        if self.product_tmpl_ids:
            products = self.product_tmpl_ids.ids
            active_model = 'product.template'
        elif self.product_ids:
            products = self.product_ids.ids
            active_model = 'product.product'

        # Build data to pass to the report
        data = {
            'picking_quantity': self.picking_quantity,
            'active_model': active_model,
            'quantity_by_product': {p: self.env[active_model].browse(p).qty_available for p in
                                    products} if self.picking_quantity == 'custom' else {p: self.custom_quantity for p
                                                                                         in products},
            'layout_wizard': self.id,
            'price_included': 'xprice' in self.print_format,
        }


        if self.picking_quantity=='picking':
            if 'zpl' in self.print_format:
                xml_id = 'stock.label_product_product'

            if self.picking_quantity == 'picking' and self.move_line_ids:
                qties = defaultdict(int)
                uom_unit = self.env.ref('uom.product_uom_categ_unit', raise_if_not_found=False)
                for line in self.move_line_ids:
                    if line.product_uom_id.category_id == uom_unit:
                        qties[line.product_id.id] += line.qty_done
                # Pass only products with some quantity done to the report
                data['quantity_by_product'] = {p: int(q) for p, q in qties.items() if q}

        return xml_id, data

"""
class AccountBankStatementLine(models.Model):
    _inherit='account.bank.statement.line'
    item_id = fields.Many2one(comodel_name="cash.items", string="بند", required=False)

    def _prepare_counterpart_move_line_vals(self, counterpart_vals, move_line=None):
        res=super()._prepare_counterpart_move_line_vals(counterpart_vals, move_line)
        if self.item_id:
            if self.item_id.account_id:
                res['account_id']=self.item_id.account_id.id
        return res





class Categ(models.Model):
    _inherit='product.category'
    cost_percentage = fields.Float(string="Cost Percentage", required=False)



class PoLine(models.Model):
    _inherit='purchase.order.line'
    product_barcode = fields.Char(string="Barcode",related='product_id.barcode',store=True)

class AccountBankStatement(models.Model):
    _inherit='account.bank.statement'
    po_config_id = fields.Many2one(
        'pos.config',related='pos_session_id.config_id',store=True)


