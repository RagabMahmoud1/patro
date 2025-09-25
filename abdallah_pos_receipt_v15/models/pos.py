from odoo import models, fields, api, _


class PosConfig(models.Model):
	_inherit = 'pos.config'

	receipt_order_brinch = fields.Char(string='اسم الفرع')
	receipt_order_mob = fields.Char(string='رقم الفرع')
	receipt_order_add = fields.Char(string='العنوان')
	enable_sales_person_receipt = fields.Boolean(string='Enable Sales Person Receipt', default=True)
	delivery_sales_person_receipt = fields.Many2many('res.users', string='Sales Person Receipt')
	pos_total_screen = fields.Boolean(string="Total Items and Quantity", default=True)
	pos_total_receipt = fields.Boolean(string="Total Items and Quantity", default=True)
class PosOrder(models.Model):
	_inherit = 'pos.order'

	sales_person_receipt = fields.Many2one('res.users', string='SalesPersonReceipt', readonly=True, )

	@api.model
	def _order_fields(self, ui_order):
		order_fields = super(PosOrder, self)._order_fields(ui_order)
		order_fields['sales_person_receipt'] = ui_order.get('delivery_sales_person_receipt_id',
															False)
		return order_fields


