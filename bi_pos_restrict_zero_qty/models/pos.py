# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class PosConfig(models.Model):
    _inherit = "pos.config"

    restrict_zero_qty = fields.Boolean(string='Restrict Zero Quantity', default=True)
    stock_location_id = fields.Many2one(
        'stock.location',
        string='Stock Location',
        compute='_compute_stock_location_id',
        store=False,
    )

    @api.depends('picking_type_id')
    def _compute_stock_location_id(self):
        for config in self:
            if config.picking_type_id and config.picking_type_id.default_location_src_id:
                config.stock_location_id = config.picking_type_id.default_location_src_id
            else:
                config.stock_location_id = False


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def get_qty_available_at_location(self, product_ids, location_id):
        """Get qty_available for products at a specific location (including children)"""
        products = self.browse(product_ids)
        if not location_id:
            return {p.id: p.qty_available for p in products}
        
        result = {}
        # Use with_context to compute qty_available for the specific location
        products_with_loc = products.with_context(location=location_id, compute_child=True)
        for product in products_with_loc:
            result[product.id] = product.qty_available
        return result

    @api.model
    def get_qty_available_at_warehouse(self, product_ids, warehouse_id):
        """Get qty_available for products at a specific warehouse (same as product info popup)"""
        products = self.browse(product_ids)
        if not warehouse_id:
            return {p.id: p.qty_available for p in products}
        
        result = {}
        # Use with_context warehouse - same as product info popup uses
        products_with_wh = products.with_context(warehouse=warehouse_id)
        for product in products_with_wh:
            result[product.id] = product.qty_available
        return result

    @api.model
    def get_warehouse_id_from_location(self, location_id):
        """Find the warehouse that owns a specific stock location"""
        if not location_id:
            return False
        
        location = self.env['stock.location'].browse(location_id)
        if not location.exists():
            return False
        
        # Search for warehouse where this location or its parent is the lot_stock_id
        warehouse = self.env['stock.warehouse'].search([
            ('lot_stock_id', '=', location_id)
        ], limit=1)
        
        if warehouse:
            return warehouse.id
        
        # Check parent locations
        parent = location.location_id
        while parent and parent.id != parent.location_id.id:
            warehouse = self.env['stock.warehouse'].search([
                ('lot_stock_id', '=', parent.id)
            ], limit=1)
            if warehouse:
                return warehouse.id
            parent = parent.location_id
        
        return False

