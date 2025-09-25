# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    fixed_discount_product_id = fields.Many2one('product.product', string='Fixed Discount Product',
                                          domain="[('sale_ok', '=', True)]",
                                          help='The product used to model the discount.')
