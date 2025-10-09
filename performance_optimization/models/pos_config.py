# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # POS Performance Settings
    limit_products_load = fields.Boolean(
        string='Limit Products to Load',
        default=True,
        help='Enable to limit the number of products loaded in POS session. '
             'Recommended for catalogs with 10,000+ products.'
    )
    
    product_load_limit = fields.Integer(
        string='Product Load Limit',
        default=1000,
        help='Maximum number of products to load initially. '
             'Other products will be loaded on-demand when searched.'
    )
    
    load_only_available_products = fields.Boolean(
        string='Load Only Available Products',
        default=True,
        help='Load only products with stock quantity > 0. '
             'Significantly improves POS session opening time.'
    )
    
    use_product_categories = fields.Many2many(
        'product.category',
        string='Product Categories to Load',
        help='If set, only products from these categories will be loaded initially. '
             'Leave empty to load from all categories.'
    )
    
    preload_favorites_only = fields.Boolean(
        string='Preload Favorite Products Only',
        default=False,
        help='Load only products marked as favorites or recently sold. '
             'All other products available via search.'
    )


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """Optimize product loading for large catalogs"""
        result = super(PosSession, self)._loader_params_product_product()
        
        config = self.config_id
        
        # Apply product loading limits
        if config.limit_products_load:
            # Modify domain to limit products
            domain = result.get('search_params', {}).get('domain', [])
            
            # Filter by available stock if enabled
            if config.load_only_available_products:
                domain.append(('qty_available', '>', 0))
            
            # Filter by categories if specified
            if config.use_product_categories:
                domain.append(('categ_id', 'child_of', config.use_product_categories.ids))
            
            # Apply limit
            search_params = result.get('search_params', {})
            search_params['domain'] = domain
            search_params['limit'] = config.product_load_limit
            
            # Order by recently sold products first
            search_params['order'] = 'write_date desc, id desc'
            
            result['search_params'] = search_params
        
        return result

    def _pos_ui_models_to_load(self):
        """Optimize models loading"""
        result = super(PosSession, self)._pos_ui_models_to_load()
        
        # Add caching hints for better performance
        config = self.config_id
        if config.limit_products_load:
            # Reduce loaded data for product.product model
            if 'product.product' in result:
                result['product.product']['load_lazily'] = True
        
        return result

    def _get_pos_ui_product_product(self, params):
        """Override to implement lazy loading of products"""
        config = self.config_id
        
        if config.limit_products_load:
            # Load limited set first
            products = self.env['product.product'].search_read(
                **params['search_params'],
                fields=params.get('fields')
            )
            return products
        
        return super(PosSession, self)._get_pos_ui_product_product(params)


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def search_product_in_pos(self, query, limit=10):
        """
        API endpoint for searching products on-demand in POS
        Used when product is not in the initially loaded set
        """
        domain = [
            '|', '|',
            ('name', 'ilike', query),
            ('default_code', 'ilike', query),
            ('barcode', '=', query),
            ('available_in_pos', '=', True),
        ]
        
        products = self.env['product.product'].search_read(
            domain,
            fields=['id', 'display_name', 'default_code', 'barcode', 
                   'list_price', 'standard_price', 'qty_available',
                   'uom_id', 'categ_id', 'taxes_id'],
            limit=limit
        )
        
        return products

