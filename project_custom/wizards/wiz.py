# -*- coding: utf-8 -*-

from odoo import fields, models

class Cash(models.TransientModel):
    _name = 'cash.wiz'
    date = fields.Date(string="Date", required=True)
    type = fields.Selection(string="Type", selection=[('in', 'Cash In'), ('out', 'Cash Out'), ], required=True)
    journal_id = fields.Many2one(comodel_name="account.journal", string="Journal", required=True)
    item_id = fields.Many2one(comodel_name="cash.items", string="بند", required=True)
    amount = fields.Float(string="Amount", required=False)
    reason = fields.Text(string="Reason", required=False)

    def make(self):
        stat=self.env['account.bank.statement'].sudo().search([('journal_id','=',self.journal_id.id),('state','=','open')],limit=1)
        if stat:
            vals= {
                'date': self.date,
                'statement_id': stat.id,
                'journal_id': self.journal_id.id,
                'amount': self.amount if self.type=='in' else -1*self.amount,
                'ref': self.item_id.name,
                'payment_ref': self.reason or '',
                'name': self.reason,
                'item_id': self.item_id.id,

            }
            self.env['account.bank.statement.line'].sudo().create(vals)
        else:
            stat = self.env['account.bank.statement'].sudo().create({'journal_id':self.journal_id.id,'name':str(self.item_id.name)+str(self.date)})
            vals = {
                'date': self.date,
                'statement_id': stat.id,
                'journal_id': self.journal_id.id,
                'amount': self.amount if self.type=='in' else -1*self.amount,
                'ref': self.item_id.name,
                'payment_ref': self.reason or '',
                'name': self.reason,
                'item_id': self.item_id.id,
            }
            self.env['account.bank.statement.line'].sudo().create(vals)




class CashItem(models.Model):
    _name='cash.items'
    name = fields.Char(string="Name", required=True)
    account_id = fields.Many2one(comodel_name='account.account', string='Account',required=True)

