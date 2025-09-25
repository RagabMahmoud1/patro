# -*- coding: utf-8 -*-

from odoo import fields, models, _
import xlsxwriter
import base64
import os


class Expenses(models.TransientModel):
    _name = 'expenses.wiz'
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
        report_name = "تقرير المصروفات"
        sheet = workbook.add_worksheet(report_name[:31])
        sheet.right_to_left()

        sheet.set_column('A:A', 30)
        sheet.set_column('B:B', 30)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 30)
        sheet.set_column('E:E', 30)
        sheet.set_column('F:F', 30)
        sheet.set_column('G:G', 30)
        sheet.write(0, 0, _('مسلسل'), bold1)
        sheet.write(0, 1, _('الفرع'), bold1)
        sheet.write(0, 2, _('التاريخ'), bold1)
        sheet.write(0, 3, _('البند'), bold1)
        sheet.write(0, 4, _('المبلغ'), bold1)
        sheet.write(0, 5, _('البيان'), bold1)
        sheet.write(0, 6, _('المستخدم'), bold1)
        row = 1
        i=1
        lines=self.get_lines()
        for line in lines:
            ll=self.env['account.bank.statement.line'].sudo().browse(int(line.get('id')))
            if ll.date>=self.date_from and ll.date<=self.date_to:
                print(">>d",line)
                sheet.write(row, 0, _(str(i)), bold)
                if line.get('pos_session_id'):
                    sheet.write(row, 1, _(str(self.env['pos.session'].sudo().browse(int(line.get('pos_session_id'))).config_id.name)), bold)
                else:
                    sheet.write(row, 1,"", bold)
                sheet.write(row, 2, _(str(ll.date)), bold)
                sheet.write(row, 3, _(str(self.env['cash.items'].sudo().browse(int(line.get('item_id'))).name)), bold)
                sheet.write(row, 4, _(str(line.get('amount'))), bold)
                sheet.write(row, 5, _(str(line.get('payment_ref'))), bold)
                sheet.write(row, 6, _(str(self.env['res.users'].sudo().browse(int(line.get('create_uid'))).name)), bold)

                row += 1
                i += 1

        workbook.close()
        with open(file_name, "rb") as file:
            file_base64 = base64.b64encode(file.read())
        data_file = file_base64

        wiz_id = self.env['excel.download'].create({
            'file_data': data_file,
            'filename': 'تقرير المصروفات'
        })
        return wiz_id

    def get_lines(self):
        query = """select account_bank_statement_line.id,account_bank_statement.date,account_bank_statement_line.amount,account_bank_statement_line.payment_ref,
                   account_bank_statement.pos_session_id,account_bank_statement_line.create_uid,date,account_bank_statement_line.item_id
                   from account_bank_statement_line
                   join account_bank_statement on account_bank_statement.id=account_bank_statement_line.statement_id
                   where account_bank_statement_line.item_id  is not NULL"""
        self.env.cr.execute(query)
        lines = self.env.cr.dictfetchall()
        return lines
































class ExcelDownload(models.TransientModel):
    _name = "excel.download"
    _description = "Partners Report Download"

    """file_data Field this is the field which contain the result of Excels function to download
     this data as a file Excel"""
    file_data = fields.Binary('Download report Excel')
    """filename Field this is the field which contain name of Excel file that we will download"""
    filename = fields.Char('Excel File', size=64)


