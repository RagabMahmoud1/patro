# -*- coding: utf-8 -*-

from odoo import api, models, tools


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _auto_init(self):
        """Add database indexes for better performance with large product catalogs"""
        res = super(ProductProduct, self)._auto_init()
        
        cr = self.env.cr
        
        # Index on barcode for faster barcode searches
        tools.create_index(
            cr, 'product_product_barcode_index',
            self._table, ['barcode']
        )
        
        # Index on default_code (internal reference) for faster searches
        tools.create_index(
            cr, 'product_product_default_code_index',
            self._table, ['default_code']
        )
        
        # Composite index on product_tmpl_id for variant lookups
        tools.create_index(
            cr, 'product_product_tmpl_active_index',
            self._table, ['product_tmpl_id', 'active']
        )
        
        return res

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """Optimized search with proper index usage"""
        if args is None:
            args = []
        
        # Use exact match first (uses index), then fallback to ilike
        if name and operator in ('=', 'ilike'):
            # Try exact barcode match first (fastest with index)
            domain = [('barcode', '=', name)]
            products = list(self._search(domain + args, limit=limit))
            if products:
                return products
            
            # Try exact default_code match
            domain = [('default_code', '=', name)]
            products = list(self._search(domain + args, limit=limit))
            if products:
                return products
        
        # Fallback to original search
        return super(ProductProduct, self)._name_search(
            name=name, args=args, operator=operator, 
            limit=limit, name_get_uid=name_get_uid
        )

