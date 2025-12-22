# -*- coding: utf-8 -*-
"""
POS Performance Settings - Limit product loading for large catalogs
"""

from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    limit_products_load = fields.Boolean(
        string='Limit Products to Load',
        default=True,
        help='Limit number of products loaded in POS session.'
    )
    
    product_load_limit = fields.Integer(
        string='Product Load Limit',
        default=1000,
        help='Maximum products to load initially.'
    )
    
    load_only_available_products = fields.Boolean(
        string='Load Only Available Products',
        default=True,
        help='Load only products with stock > 0.'
    )


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """Optimize product loading for large catalogs"""
        result = super(PosSession, self)._loader_params_product_product()
        
        config = self.config_id
        
        if config.limit_products_load:
            domain = result.get('search_params', {}).get('domain', [])
            
            if config.load_only_available_products:
                domain.append(('qty_available', '>', 0))
            
            search_params = result.get('search_params', {})
            search_params['domain'] = domain
            search_params['limit'] = config.product_load_limit
            search_params['order'] = 'write_date desc, id desc'
            result['search_params'] = search_params
        
        return result
