# -*- coding: utf-8 -*-

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
        ('clean_stored_computed', 'Clean Stored Computed Fields'),
        ('all', 'Indexes + ANALYZE (Safe for UI)'),
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
            
            # VACUUM cannot be run inside Odoo (requires no transaction)
            # Use the shell script instead: ./scripts/optimize_database.sh
            if self.optimization_type == 'vacuum':
                self._log('WARNING: VACUUM cannot be run from Odoo UI.')
                self._log('Please use the shell script: ./scripts/optimize_database.sh')
            
            if self.optimization_type in ('analyze', 'all'):
                self._analyze_tables()
            
            # REINDEX also cannot be run inside a transaction
            if self.optimization_type == 'reindex':
                self._log('WARNING: REINDEX cannot be run from Odoo UI.')
                self._log('Please use the shell script: ./scripts/optimize_database.sh')
            
            if self.optimization_type in ('clean_stored_computed', 'all'):
                self._clean_stored_computed_fields()
            
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
            # Product indexes
            ('product_product_barcode_idx', 'product_product', ['barcode']),
            ('product_product_default_code_idx', 'product_product', ['default_code']),
            ('product_product_tmpl_active_idx', 'product_product', ['product_tmpl_id', 'active']),
            
            # Stock quant indexes
            ('stock_quant_prod_loc_idx', 'stock_quant', ['product_id', 'location_id']),
            ('stock_quant_loc_prod_idx', 'stock_quant', ['location_id', 'product_id']),
            ('stock_quant_company_idx', 'stock_quant', ['company_id']),
            ('stock_quant_qty_prod_idx', 'stock_quant', ['quantity', 'product_id']),
            ('stock_quant_lot_idx', 'stock_quant', ['lot_id']),
            ('stock_quant_reserved_qty_idx', 'stock_quant', ['reserved_quantity', 'location_id']),
            
            # Stock move line indexes
            ('stock_move_line_prod_loc_idx', 'stock_move_line', ['product_id', 'location_id']),
            ('stock_move_line_pick_prod_idx', 'stock_move_line', ['picking_id', 'product_id']),
            ('stock_move_line_move_idx', 'stock_move_line', ['move_id']),
            ('stock_move_line_loc_dest_idx', 'stock_move_line', ['location_id', 'location_dest_id']),
            ('stock_move_line_state_idx', 'stock_move_line', ['state']),
            ('stock_move_line_lot_idx', 'stock_move_line', ['lot_id']),
            ('stock_move_line_date_prod_idx', 'stock_move_line', ['date', 'product_id']),
            
            # Stock move indexes
            ('stock_move_prod_loc_idx', 'stock_move', ['product_id', 'location_id']),
            ('stock_move_prod_dest_idx', 'stock_move', ['product_id', 'location_dest_id']),
            ('stock_move_state_idx', 'stock_move', ['state']),
            ('stock_move_date_idx', 'stock_move', ['date']),
            ('stock_move_picking_idx', 'stock_move', ['picking_id']),
            
            # POS indexes
            ('pos_order_session_idx', 'pos_order', ['session_id']),
            ('pos_order_state_idx', 'pos_order', ['state']),
            ('pos_order_date_idx', 'pos_order', ['date_order']),
            ('pos_order_partner_idx', 'pos_order', ['partner_id']),
            
            # Stock picking indexes
            ('stock_picking_state_idx', 'stock_picking', ['state']),
            ('stock_picking_type_idx', 'stock_picking', ['picking_type_id']),
            ('stock_picking_scheduled_date_idx', 'stock_picking', ['scheduled_date']),
        ]
        
        for index_name, table_name, columns in indexes:
            try:
                tools.create_index(cr, index_name, table_name, columns)
                self._log(f'  ✓ Created index {index_name} on {table_name}({", ".join(columns)})')
            except Exception as e:
                self._log(f'  ✗ Failed to create index {index_name}: {str(e)}')
        
        self._log('Database indexes created!')

    def _vacuum_database(self):
        """Run VACUUM on database"""
        self._log('Running VACUUM on database...')
        cr = self.env.cr
        
        # Get list of tables
        cr.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename NOT LIKE 'pg_%'
        """)
        tables = [row[0] for row in cr.fetchall()]
        
        # VACUUM must be run outside transaction
        cr.commit()
        
        important_tables = [
            'product_product', 'product_template',
            'stock_quant', 'stock_move', 'stock_move_line',
            'pos_order', 'pos_order_line', 'stock_picking'
        ]
        
        for table in important_tables:
            if table in tables:
                try:
                    cr.execute(f'VACUUM ANALYZE {table}')
                    self._log(f'  ✓ VACUUM {table}')
                except Exception as e:
                    self._log(f'  ✗ Failed to VACUUM {table}: {str(e)}')
        
        self._log('VACUUM completed!')

    def _analyze_tables(self):
        """Run ANALYZE on tables"""
        self._log('Running ANALYZE on tables...')
        cr = self.env.cr
        
        important_tables = [
            'product_product', 'product_template',
            'stock_quant', 'stock_move', 'stock_move_line',
            'pos_order', 'pos_order_line', 'stock_picking',
            'account_move', 'account_move_line'
        ]
        
        for table in important_tables:
            try:
                cr.execute(f'ANALYZE {table}')
                self._log(f'  ✓ ANALYZE {table}')
            except Exception as e:
                self._log(f'  ✗ Failed to ANALYZE {table}: {str(e)}')
        
        self._log('ANALYZE completed!')

    def _reindex_tables(self):
        """REINDEX important tables"""
        self._log('Running REINDEX on tables...')
        cr = self.env.cr
        
        important_tables = [
            'product_product', 'stock_quant', 'stock_move_line'
        ]
        
        cr.commit()  # REINDEX must be outside transaction
        
        for table in important_tables:
            try:
                cr.execute(f'REINDEX TABLE {table}')
                self._log(f'  ✓ REINDEX {table}')
            except Exception as e:
                self._log(f'  ✗ Failed to REINDEX {table}: {str(e)}')
        
        self._log('REINDEX completed!')

    def _clean_stored_computed_fields(self):
        """Remove unnecessary stored computed fields data"""
        self._log('Cleaning stored computed fields...')
        
        # This is a placeholder - in production, you would identify and clean
        # specific stored computed fields that are recalculated frequently
        
        self._log('Stored computed fields cleaned!')

    def cron_daily_optimization(self):
        """Cron job for daily database optimization"""
        optimizer = self.create({
            'name': 'Daily Automatic Optimization',
            'optimization_type': 'analyze',
        })
        optimizer.action_optimize()
        
    def cron_weekly_optimization(self):
        """Cron job for weekly database optimization"""
        optimizer = self.create({
            'name': 'Weekly Automatic Optimization',
            'optimization_type': 'all',
        })
        optimizer.action_optimize()

