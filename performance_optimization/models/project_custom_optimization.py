# -*- coding: utf-8 -*-

from odoo import api, models, fields


class StockQuantOptimized(models.Model):
    """
    Optimize the stock.quant model from project_custom module
    Remove unnecessary stored computed fields that cause performance issues
    """
    _inherit = 'stock.quant'

    # Override to remove store=True from heavy computed fields
    # These fields recalculate too frequently with 28K products
    ore_id = fields.Many2one(
        comodel_name="product.ore",
        string="نوع الخامة",
        related='product_id.ore_id',
        store=False  # Changed from True to False
    )
    
    session_id = fields.Many2one(
        comodel_name="product.session",
        string="الموسم",
        related='product_id.session_id',
        store=False  # Changed from True to False
    )
    
    categ_id = fields.Many2one(
        comodel_name="product.category",
        string="Category",
        related='product_id.categ_id',
        store=False  # Changed from True to False
    )
    
    color = fields.Char(
        string='Color',
        related='product_id.color',
        store=False  # Changed from True to False
    )
    
    size = fields.Char(
        string='Size',
        related='product_id.size',
        store=False  # Changed from True to False
    )
    
    model_year = fields.Char(
        string='Model Year',
        related='product_id.model_year',
        store=False  # Changed from True to False
    )
    
    list_price = fields.Float(
        related='product_id.list_price',
        store=False  # Changed from True to False
    )
    
    standard_price = fields.Float(
        related='product_id.standard_price',
        store=False  # Changed from True to False
    )
    
    virtual_available = fields.Float(
        related='product_id.virtual_available',
        store=False  # Changed from True to False
    )
    
    product_tmpl_id2 = fields.Many2one(
        'product.template',
        string='Product Template',
        related='product_id.product_tmpl_id',
        store=False  # Changed from True to False
    )


class StockMoveLineOptimized(models.Model):
    """
    Optimize the stock.move.line model from project_custom module
    """
    _inherit = 'stock.move.line'

    # Override to remove store=True from heavy computed fields
    ore_id = fields.Many2one(
        comodel_name="product.ore",
        string="نوع الخامة",
        related='product_id.ore_id',
        store=False  # Changed from True to False
    )
    
    session_id = fields.Many2one(
        comodel_name="product.session",
        string="الموسم",
        related='product_id.session_id',
        store=False  # Changed from True to False
    )
    
    categ_id = fields.Many2one(
        comodel_name="product.category",
        string="Category",
        related='product_id.categ_id',
        store=False  # Changed from True to False
    )
    
    color = fields.Char(
        string='Color',
        related='product_id.color',
        store=False  # Changed from True to False
    )
    
    size = fields.Char(
        string='Size',
        related='product_id.size',
        store=False  # Changed from True to False
    )
    
    model_year = fields.Char(
        string='Model Year',
        related='product_id.model_year',
        store=False  # Changed from True to False
    )


class ProductProductOptimized(models.Model):
    """
    Optimize product.product computations
    """
    _inherit = 'product.product'

    # Override color and size to add indexes
    color = fields.Char(
        string='Color',
        compute='_calc_color',
        store=True,
        index=True  # Add index for faster filtering
    )
    
    size = fields.Char(
        string='Size',
        compute='_calc_color',
        store=True,
        index=True  # Add index for faster filtering
    )

    @api.depends('product_template_variant_value_ids', 
                 'product_template_variant_value_ids.attribute_id.is_color',
                 'product_template_variant_value_ids.attribute_id.is_size')
    def _calc_color(self):
        """Optimized color/size calculation with better performance"""
        for rec in self:
            color = False
            size = False
            
            # Use cached values when possible
            for value in rec.product_template_variant_value_ids:
                attr = value.product_attribute_value_id.attribute_id
                if attr.is_color and not color:
                    color = value.product_attribute_value_id.name
                if attr.is_size and not size:
                    size = value.product_attribute_value_id.name
                
                # Early exit if both found
                if color and size:
                    break
            
            rec.color = color
            rec.size = size

