from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Payment(models.Model):
    _inherit='account.payment'
    use_discount = fields.Boolean(string="Use Discount")
    discount_name = fields.Char(string="Discount Name", required=False)
    discount_type = fields.Selection(string="Discount Type", selection=[('amount', 'Amount'), ('percentage', 'Percentage'), ],
                                 required=False)
    discount = fields.Float(string="Discount", required=False)
    amount2 = fields.Float(string="Amount Before Discount", required=False)
    debit = fields.Monetary(default=0.0,related='partner_id.debit',store=True )
    credit = fields.Monetary(default=0.0,related='partner_id.credit',store=True )

    @api.onchange('use_discount','discount_type','discount','amount2')
    def onchange_amount2(self):
        if self.use_discount:
            if self.discount_type=='amount':
                self.amount=self.amount2-self.discount

            if self.discount_type == 'percentage':
                self.amount = self.amount2-(self.amount2 *(self.discount/100))
