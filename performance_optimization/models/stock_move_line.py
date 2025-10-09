# -*- coding: utf-8 -*-

from odoo import api, models, tools, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    # Remove store=True from computed fields to avoid unnecessary database writes
    # These can be computed on-the-fly when needed
    qty_available = fields.Float(
        string="Quantity On Hand",
        compute='_calc_qty_available',
        store=False  # Changed from True to False for better performance
    )

    @api.model
    def _auto_init(self):
        """Add database indexes for faster stock move queries"""
        res = super(StockMoveLine, self)._auto_init()
        
        cr = self.env.cr
        
        # Composite index on product_id + location_id
        tools.create_index(
            cr, 'stock_move_line_product_location_index',
            self._table, ['product_id', 'location_id']
        )
        
        # Composite index on picking_id + product_id
        tools.create_index(
            cr, 'stock_move_line_picking_product_index',
            self._table, ['picking_id', 'product_id']
        )
        
        # Index on move_id for faster joins
        tools.create_index(
            cr, 'stock_move_line_move_index',
            self._table, ['move_id']
        )
        
        # Composite index on location_id + location_dest_id for transfer queries
        tools.create_index(
            cr, 'stock_move_line_location_dest_index',
            self._table, ['location_id', 'location_dest_id']
        )
        
        # Index on state for filtering
        tools.create_index(
            cr, 'stock_move_line_state_index',
            self._table, ['state']
        )
        
        # Index on lot_id for lot tracking
        tools.create_index(
            cr, 'stock_move_line_lot_index',
            self._table, ['lot_id']
        )
        
        # Composite index on date for time-based queries
        tools.create_index(
            cr, 'stock_move_line_date_product_index',
            self._table, ['date', 'product_id']
        )
        
        return res

    @api.depends('product_id.qty_available', 'picking_id.location_id')
    def _calc_qty_available(self):
        """Optimized qty_available calculation with batching"""
        # Group by location and product to reduce queries
        location_product_map = {}
        for line in self:
            if line.picking_id and line.picking_id.location_id:
                key = (line.picking_id.location_id.id, line.product_id.id)
                if key not in location_product_map:
                    location_product_map[key] = []
                location_product_map[key].append(line)
        
        # Batch query for all location-product combinations
        for (location_id, product_id), lines in location_product_map.items():
            quants = self.env['stock.quant'].read_group(
                [('location_id', '=', location_id), ('product_id', '=', product_id)],
                ['quantity:sum'],
                []
            )
            qty = quants[0]['quantity'] if quants and quants[0].get('quantity') else 0
            qty_available = max(0, qty)
            
            for line in lines:
                line.qty_available = qty_available
        
        # Handle lines without picking_id
        for line in self:
            if line.id not in sum(location_product_map.values(), []):
                line.qty_available = 0

    @api.constrains('qty_done', 'picking_id.location_id')
    def check_qty_done_hand(self):
        """Optimized constraint check with reduced queries"""
        # Batch all checks to reduce database queries
        lines_to_check = self.filtered(
            lambda l: l.picking_id and l.picking_id.picking_type_code in ('outgoing', 'internal')
        )
        
        if not lines_to_check:
            return
        
        # Group by location and product
        location_product_lines = {}
        for line in lines_to_check:
            key = (line.picking_id.location_id.id, line.product_id.id)
            if key not in location_product_lines:
                location_product_lines[key] = []
            location_product_lines[key].append(line)
        
        # Batch query for all combinations
        for (location_id, product_id), lines in location_product_lines.items():
            quants = self.env['stock.quant'].read_group(
                [('location_id', '=', location_id), ('product_id', '=', product_id)],
                ['quantity:sum'],
                []
            )
            qty_available = quants[0]['quantity'] if quants and quants[0].get('quantity') else 0
            
            for line in lines:
                if line.qty_done > qty_available:
                    from odoo.exceptions import ValidationError
                    raise ValidationError("Order Qty Greater Than Quantity On Hand")

