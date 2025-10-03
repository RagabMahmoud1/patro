from odoo import models, fields

class ProductModel(models.Model):
    _name = 'product.model'
    _description = 'Product Model'

    name = fields.Char(string='Model Name', required=True)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    vendor_id = fields.Many2one('res.partner', string='Vendor')
    model_id = fields.Many2one('product.model', string='Model')

class ProductProduct(models.Model):
    _inherit = 'product.product'

    vendor_id = fields.Many2one('res.partner', related='product_tmpl_id.vendor_id', store=True, string='Vendor')
    model_id = fields.Many2one('product.model', related='product_tmpl_id.model_id', store=True, string='Model')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    vendor_id = fields.Many2one('res.partner', related='product_id.vendor_id', store=True, readonly=True, string='Vendor')
    model_id = fields.Many2one('product.model', related='product_id.model_id', store=True, readonly=True, string='Model')

# -*- coding: utf-8 -*-
from odoo import fields, models

# -*- coding: utf-8 -*-
from odoo import fields, models

# -*- coding: utf-8 -*-
from odoo import fields, models

class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    vendor_id = fields.Many2one('res.partner', string='Vendor', readonly=True)
    model_id = fields.Many2one('product.model', string='Model', readonly=True)
    product_cost = fields.Float(string="Cost Price", readonly=True)
    qty_on_hand = fields.Float(
            string="Quantity On Hand",
            readonly=True
        )
    def _select(self):
        return super()._select() + """
            , pt.vendor_id as vendor_id
            , pt.model_id as model_id
            , pt.list_price as product_cost
            , l.qty_available as qty_on_hand

            
        """

    def _group_by(self):
        return super()._group_by() + """
            , pt.vendor_id
            , pt.model_id
            , pt.list_price
            ,l.qty_available
        """
