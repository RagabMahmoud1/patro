# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_model = fields.Char(
        string='Model',
        related='product_id.product_tmpl_id.model',
        store=False,
        readonly=True,
    )
    product_vendors = fields.Char(
        string='Vendors',
        compute='_compute_product_vendors',
        store=False,
        readonly=True,
    )

    @api.depends('product_id', 'product_id.product_tmpl_id', 'product_id.product_tmpl_id.seller_ids', 'product_id.product_tmpl_id.seller_ids.name', 'product_id.product_tmpl_id.seller_ids.name.name')
    def _compute_product_vendors(self):
        for quant in self:
            tmpl = quant.product_id.product_tmpl_id
            vendor_names = tmpl.seller_ids.mapped('name.name')
            quant.product_vendors = ', '.join(vendor_names)


