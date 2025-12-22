# -*- coding: utf-8 -*-
"""
Database Optimizer - Creates all performance indexes
"""

from odoo import api, fields, models, tools
import logging

_logger = logging.getLogger(__name__)


class DatabaseOptimizer(models.TransientModel):
    _name = 'database.optimizer'
    _description = 'Database Optimization Utilities'

    name = fields.Char(string='Optimization Name', required=True, default='Database Optimization')
    optimization_type = fields.Selection([
        ('indexes', 'Create/Update Indexes'),
        ('analyze', 'ANALYZE Tables'),
        ('all', 'Indexes + ANALYZE'),
    ], string='Optimization Type', default='all', required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('error', 'Error'),
    ], default='draft', string='State')
    
    log = fields.Text(string='Optimization Log', readonly=True)

    def _log(self, message):
        """Add message to log"""
        _logger.info(message)
        current_log = self.log or ''
        self.log = current_log + '\n' + message

    def action_optimize(self):
        """Run database optimization"""
        self.write({'state': 'running', 'log': 'Starting optimization...'})
        
        try:
            if self.optimization_type in ('indexes', 'all'):
                self._create_indexes()
            
            if self.optimization_type in ('analyze', 'all'):
                self._analyze_tables()
            
            self.write({'state': 'done'})
            self._log('Optimization completed successfully!')
            
        except Exception as e:
            self.write({'state': 'error'})
            self._log(f'ERROR: {str(e)}')
            raise

    def _create_indexes(self):
        """Create all performance indexes"""
        self._log('Creating database indexes...')
        cr = self.env.cr

        indexes = [
            # ============================================
            # Product Product Indexes
            # ============================================
            ('product_product_barcode_idx', 'product_product', ['barcode']),
            ('product_product_default_code_idx', 'product_product', ['default_code']),
            ('product_product_tmpl_active_idx', 'product_product', ['product_tmpl_id', 'active']),
            ('product_product_color_idx', 'product_product', ['color']),
            ('product_product_size_idx', 'product_product', ['size']),
            ('product_product_ore_id_idx', 'product_product', ['ore_id']),
            ('product_product_session_id_idx', 'product_product', ['session_id']),
            
            # ============================================
            # Product Template Indexes
            # ============================================
            ('product_template_ore_id_idx', 'product_template', ['ore_id']),
            ('product_template_session_id_idx', 'product_template', ['session_id']),
            ('product_template_model_year_idx', 'product_template', ['model_year']),
            ('product_template_categ_ore_idx', 'product_template', ['categ_id', 'ore_id']),
            
            # ============================================
            # Stock Quant Indexes (Critical for reports)
            # ============================================
            ('stock_quant_prod_loc_idx', 'stock_quant', ['product_id', 'location_id']),
            ('stock_quant_loc_prod_idx', 'stock_quant', ['location_id', 'product_id']),
            ('stock_quant_company_idx', 'stock_quant', ['company_id']),
            ('stock_quant_qty_prod_idx', 'stock_quant', ['quantity', 'product_id']),
            ('stock_quant_lot_idx', 'stock_quant', ['lot_id']),
            ('stock_quant_ore_id_idx', 'stock_quant', ['ore_id']),
            ('stock_quant_session_id_idx', 'stock_quant', ['session_id']),
            ('stock_quant_categ_id_idx', 'stock_quant', ['categ_id']),
            ('stock_quant_color_idx', 'stock_quant', ['color']),
            ('stock_quant_size_idx', 'stock_quant', ['size']),
            
            # ============================================
            # Stock Move Line Indexes
            # ============================================
            ('stock_move_line_prod_loc_idx', 'stock_move_line', ['product_id', 'location_id']),
            ('stock_move_line_pick_prod_idx', 'stock_move_line', ['picking_id', 'product_id']),
            ('stock_move_line_move_idx', 'stock_move_line', ['move_id']),
            ('stock_move_line_state_idx', 'stock_move_line', ['state']),
            ('stock_move_line_date_prod_idx', 'stock_move_line', ['date', 'product_id']),
            ('stock_move_line_ore_id_idx', 'stock_move_line', ['ore_id']),
            ('stock_move_line_session_id_idx', 'stock_move_line', ['session_id']),
            ('stock_move_line_categ_id_idx', 'stock_move_line', ['categ_id']),
            
            # ============================================
            # Stock Move Indexes
            # ============================================
            ('stock_move_prod_loc_idx', 'stock_move', ['product_id', 'location_id']),
            ('stock_move_state_idx', 'stock_move', ['state']),
            ('stock_move_date_idx', 'stock_move', ['date']),
            ('stock_move_picking_idx', 'stock_move', ['picking_id']),
            
            # ============================================
            # POS Order Indexes
            # ============================================
            ('pos_order_session_idx', 'pos_order', ['session_id']),
            ('pos_order_state_idx', 'pos_order', ['state']),
            ('pos_order_date_idx', 'pos_order', ['date_order']),
            
            # ============================================
            # Stock Picking Indexes
            # ============================================
            ('stock_picking_state_idx', 'stock_picking', ['state']),
            ('stock_picking_type_idx', 'stock_picking', ['picking_type_id']),
        ]

        def _column_exists(table, column):
            cr.execute("""
                SELECT 1 FROM information_schema.columns
                 WHERE table_name=%s AND column_name=%s
            """, (table, column))
            return bool(cr.fetchone())

        for index_name, table_name, columns in indexes:
            try:
                missing = [c for c in columns if not _column_exists(table_name, c)]
                if missing:
                    self._log(f'  ⚠ {index_name}: skipped (missing columns: {", ".join(missing)})')
                    continue

                tools.create_index(cr, index_name, table_name, columns)
                self._log(f'  ✓ {index_name}')
            except Exception as e:
                # ensure cursor is usable after a failed statement
                cr.rollback()
                self._log(f'  ✗ {index_name}: {str(e)}')

        self._log('Indexes created!')

    def _analyze_tables(self):
        """Run ANALYZE on tables"""
        self._log('Running ANALYZE...')
        cr = self.env.cr
        
        tables = [
            'product_product', 'product_template',
            'stock_quant', 'stock_move', 'stock_move_line',
            'pos_order', 'stock_picking',
        ]
        
        for table in tables:
            try:
                cr.execute(f'ANALYZE {table}')
                self._log(f'  ✓ {table}')
            except Exception as e:
                self._log(f'  ✗ {table}: {str(e)}')
        
        self._log('ANALYZE completed!')

    def cron_daily_optimization(self):
        """Cron job for daily optimization"""
        optimizer = self.create({
            'name': 'Daily Optimization',
            'optimization_type': 'analyze',
        })
        optimizer.action_optimize()
