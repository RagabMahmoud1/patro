# -*- coding: utf-8 -*-

from odoo import fields, models, _,api
import xlsxwriter
import base64
import os
from datetime import datetime, date, timedelta
from dateutil import relativedelta
from odoo.osv.expression import AND
import pytz

class Sales(models.TransientModel):
    _name = 'sales.wiz'
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    # item_id = fields.Many2one(comodel_name="cash.items", string="بند", required=False)
    # config_ids = fields.Many2many(comodel_name="pos.config", relation="exp_poc",  string="الفروع", required=True)


    def print_excel(self):
        self.ensure_one()
        wiz_id = self.export_data()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Download Excel'),
            'res_model': 'excel.download',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz_id.id,
            'target': 'new'
        }

    def get_expes(self,po_config_id,day):
        query = """select sum(account_bank_statement_line.amount) as total
                      from account_bank_statement_line
                      join account_bank_statement on account_bank_statement.id=account_bank_statement_line.statement_id
                      where account_bank_statement_line.item_id  is not NULL and account_bank_statement.po_config_id={po_config_id} 
                      and date(account_bank_statement.date) =\'{date}\'""".format(po_config_id=po_config_id,date=day)
        print(">>D",query)
        self.env.cr.execute(query)
        lines = self.env.cr.dictfetchall()
        sum=0
        if lines:
            sum=lines[0]['total']
        return sum

    # journal_user
    def export_data(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        file_name = path + '/temp'
        workbook = xlsxwriter.Workbook(file_name, {'in_memory': True})
        bold1 = workbook.add_format(
            {'bold': True, 'locked': True, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 14,
             'bg_color': '#FFF58C'})

        bold = workbook.add_format(
            {'bold': True, 'locked': True, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 12})
        report_name = "تقرير المبيعات"
        sheet = workbook.add_worksheet(report_name[:31])
        sheet.right_to_left()


        sheet.write(0, 0, _('التاريخ'), bold1)
        sheet.set_column(0,0,20)
        col=1
        for pos in self.env['pos.config'].sudo().search([]):
            sheet.write(0, col,pos.name, bold1)
            sheet.set_column(col, col, 20)
            col+=1
        sheet.write(0, col, _('صافي الفروع'), bold1)
        sheet.set_column(col, col, 20)
        row = 1

        for date in self.daterange(self.date_from,self.date_to):
            col = 1
            sum = 0
            sheet.write(row, 0, str(date), bold)
            for pos in self.env['pos.config'].sudo().search([]):
                lines = self.get_lines(pos.id,date)
                print(">D>>",)
                exps=self.get_expes(pos.id,date) or 0
                if exps:
                    st="مصروفات:"+str(exps)+"\n"
                else:
                    st=""
                for line in lines:
                    sum += line.get('total')
                    sum += exps
                    if line.get('payment_method_id'):
                        payment_method_id=self.env['pos.payment.method'].sudo().browse(line.get('payment_method_id')).name

                    st+=str(payment_method_id)+":"+str(line.get('total'))+"\n"



                sheet.write(row, col, st, bold)
                sheet.set_row(row, 80)
                col += 1
            sheet.write(row, col, sum, bold)
            row+=1

        workbook.close()
        with open(file_name, "rb") as file:
            file_base64 = base64.b64encode(file.read())
        data_file = file_base64

        wiz_id = self.env['excel.download'].create({
            'file_data': data_file,
            'filename': 'تقرير المبيعات'
        })
        return wiz_id

    def get_lines(self,config_id,date):
        query = """select  pos_payment.payment_method_id,sum(pos_payment.amount) as total from pos_payment
                    join pos_order on pos_order.id=pos_payment.pos_order_id
                    join pos_session on pos_session.id=pos_order.session_id
                    where pos_session.config_id ={config_id}  and pos_order.state='done' and pos_order.date_order>=\'{date_from}\'
                    group by pos_payment.payment_method_id
                    """.format(config_id=config_id,date_from=date)
        self.env.cr.execute(query)
        lines = self.env.cr.dictfetchall()
        print(">",query)
        return lines


    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)












class PosDetails(models.TransientModel):
    _inherit = 'pos.details.wizard'

    date_fr = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)

    @api.onchange('date_fr')
    def onchange_date_fr(self):
        if self.date_fr:
            self.start_date=datetime(self.date_fr.year,self.date_fr.month,self.date_fr.day,7,0,0)

    @api.onchange('date_to')
    def onchange_date_to(self):
        if self.date_to:
            self.end_date=datetime(self.date_to.year,self.date_to.month,self.date_to.day+1,4,0,0)
















class ReportSaleDetails(models.AbstractModel):

    _inherit = 'report.point_of_sale.report_saledetails'


    @api.model
    def get_sale_details(self, date_start=False, date_stop=False, config_ids=False, session_ids=False):
        """ Serialise the orders of the requested time period, configs and sessions.

        :param date_start: The dateTime to start, default today 00:00:00.
        :type date_start: str.
        :param date_stop: The dateTime to stop, default date_start + 23:59:59.
        :type date_stop: str.
        :param config_ids: Pos Config id's to include.
        :type config_ids: list of numbers.
        :param session_ids: Pos Config id's to include.
        :type session_ids: list of numbers.

        :returns: dict -- Serialised sales.
        """
        domain = [('state', 'in', ['paid','invoiced','done'])]

        if (session_ids):
            domain = AND([domain, [('session_id', 'in', session_ids)]])
        else:
            if date_start:
                date_start = fields.Datetime.from_string(date_start)
            else:
                # start by default today 00:00:00
                user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
                today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
                date_start = today.astimezone(pytz.timezone('UTC'))

            if date_stop:
                date_stop = fields.Datetime.from_string(date_stop)
                # avoid a date_stop smaller than date_start
                if (date_stop < date_start):
                    date_stop = date_start + timedelta(days=1, seconds=-1)
            else:
                # stop by default today 23:59:59
                date_stop = date_start + timedelta(days=1, seconds=-1)

            domain = AND([domain,
                [('date_order', '>=', fields.Datetime.to_string(date_start)),
                ('date_order', '<=', fields.Datetime.to_string(date_stop))]
            ])

            if config_ids:
                domain = AND([domain, [('config_id', 'in', config_ids)]])

        orders = self.env['pos.order'].search(domain)

        user_currency = self.env.company.currency_id

        total = 0.0
        products_sold = {}
        taxes = {}
        for order in orders:
            if user_currency != order.pricelist_id.currency_id:
                total += order.pricelist_id.currency_id._convert(
                    order.amount_total, user_currency, order.company_id, order.date_order or fields.Date.today())
            else:
                total += order.amount_total
            currency = order.session_id.currency_id

            for line in order.lines:
                key = (line.product_id, line.price_unit, line.discount)
                products_sold.setdefault(key, 0.0)
                products_sold[key] += line.qty

                if line.tax_ids_after_fiscal_position:
                    line_taxes = line.tax_ids_after_fiscal_position.sudo().compute_all(line.price_unit * (1-(line.discount or 0.0)/100.0), currency, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
                    for tax in line_taxes['taxes']:
                        taxes.setdefault(tax['id'], {'name': tax['name'], 'tax_amount':0.0, 'base_amount':0.0})
                        taxes[tax['id']]['tax_amount'] += tax['amount']
                        taxes[tax['id']]['base_amount'] += tax['base']
                else:
                    taxes.setdefault(0, {'name': _('No Taxes'), 'tax_amount':0.0, 'base_amount':0.0})
                    taxes[0]['base_amount'] += line.price_subtotal_incl

        payment_ids = self.env["pos.payment"].search([('pos_order_id', 'in', orders.ids)]).ids
        if payment_ids:
            self.env.cr.execute("""
                SELECT method.name, sum(amount) total
                FROM pos_payment AS payment,
                     pos_payment_method AS method
                WHERE payment.payment_method_id = method.id
                    AND payment.id IN %s
                GROUP BY method.name
            """, (tuple(payment_ids),))
            payments = self.env.cr.dictfetchall()
        else:
            payments = []

        return {
            'currency_precision': user_currency.decimal_places,
            'total_paid': user_currency.round(total),
            'payments': payments,
            'company_name': self.env.company.name,
            'taxes': list(taxes.values()),
            'products': sorted([{
                'product_id': product.id,
                'product_name': product.display_name,
                'code': product.default_code,
                'quantity': qty,
                'price_unit': price_unit,
                'discount': discount,
                'uom': product.uom_id.name
            } for (product, price_unit, discount), qty in products_sold.items()], key=lambda l: l['product_name'])
        }







