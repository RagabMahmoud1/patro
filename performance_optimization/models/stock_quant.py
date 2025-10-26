# -*- coding: utf-8 -*-

from odoo import api, models, tools, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    # Show product template fields on quants
    model = fields.Char(string='Model', related='product_id.product_tmpl_id.model', store=True)
    vendors_names = fields.Char(string='Vendors', compute='_compute_vendors_names', store=False)

    @api.model
    def _auto_init(self):
        """Add database indexes for faster stock queries"""
        res = super(StockQuant, self)._auto_init()
        
        cr = self.env.cr
        
        # Composite index on product_id + location_id (most common query)
        tools.create_index(
            cr, 'stock_quant_product_location_index',
            self._table, ['product_id', 'location_id']
        )
        
        # Composite index on location_id + product_id (for location-based queries)
        tools.create_index(
            cr, 'stock_quant_location_product_index',
            self._table, ['location_id', 'product_id']
        )
        
        # Index on company_id for multi-company setups
        tools.create_index(
            cr, 'stock_quant_company_index',
            self._table, ['company_id']
        )
        
        # Composite index for quantity queries (non-zero stock)
        tools.create_index(
            cr, 'stock_quant_quantity_product_index',
            self._table, ['quantity', 'product_id']
        )
        
        # Index on lot_id for lot/serial number tracking
        tools.create_index(
            cr, 'stock_quant_lot_index',
            self._table, ['lot_id']
        )
        
        # Composite index for reserved quantity queries
        tools.create_index(
            cr, 'stock_quant_reserved_quantity_index',
            self._table, ['reserved_quantity', 'location_id']
        )
        
        return res

    def _gather(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False):
        """Optimized gather method with better query performance"""
        # Use read_group when possible to reduce queries
        if not strict and not lot_id and not package_id and not owner_id:
            # Use index-optimized query
            domain = [
                ('product_id', '=', product_id.id),
                ('location_id', 'child_of', location_id.id),
            ]
            return self.search(domain, order='id')
        
        return super(StockQuant, self)._gather(
            product_id, location_id, lot_id=lot_id, 
            package_id=package_id, owner_id=owner_id, strict=strict
        )

    def _compute_vendors_names(self):
        for rec in self:
            tmpl = rec.product_id.product_tmpl_id
            names = ', '.join(tmpl.vendors.mapped('name')) if hasattr(tmpl, 'vendors') and tmpl.vendors else ''
            rec.vendors_names = names

