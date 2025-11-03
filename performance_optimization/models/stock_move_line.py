# -*- coding: utf-8 -*-

from odoo import api, models, tools, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'



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
