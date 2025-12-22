-- ============================================
-- Performance Indexes for Odoo 15
-- Run this script directly on your database
-- ============================================

-- ============================================
-- Product Product Indexes
-- ============================================
CREATE INDEX CONCURRENTLY IF NOT EXISTS product_product_barcode_idx 
    ON product_product (barcode) WHERE barcode IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS product_product_default_code_idx 
    ON product_product (default_code) WHERE default_code IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS product_product_tmpl_active_idx 
    ON product_product (product_tmpl_id, active);

CREATE INDEX CONCURRENTLY IF NOT EXISTS product_product_color_idx 
    ON product_product (color) WHERE color IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS product_product_size_idx 
    ON product_product (size) WHERE size IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS product_product_ore_id_idx 
    ON product_product (ore_id) WHERE ore_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS product_product_session_id_idx 
    ON product_product (session_id) WHERE session_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS product_product_tmpl_color_size_idx 
    ON product_product (product_tmpl_id, color, size);

-- ============================================
-- Product Template Indexes
-- ============================================
CREATE INDEX CONCURRENTLY IF NOT EXISTS product_template_ore_id_idx 
    ON product_template (ore_id) WHERE ore_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS product_template_session_id_idx 
    ON product_template (session_id) WHERE session_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS product_template_model_year_idx 
    ON product_template (model_year) WHERE model_year IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS product_template_categ_ore_idx 
    ON product_template (categ_id, ore_id);

-- ============================================
-- Stock Quant Indexes (Critical for Stock Reports)
-- ============================================
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_product_location_idx 
    ON stock_quant (product_id, location_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_location_product_idx 
    ON stock_quant (location_id, product_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_company_idx 
    ON stock_quant (company_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_quantity_product_idx 
    ON stock_quant (quantity, product_id) WHERE quantity != 0;

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_lot_idx 
    ON stock_quant (lot_id) WHERE lot_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_reserved_qty_idx 
    ON stock_quant (reserved_quantity, location_id) WHERE reserved_quantity > 0;

-- Custom fields indexes (from project_custom)
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_ore_id_idx 
    ON stock_quant (ore_id) WHERE ore_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_session_id_idx 
    ON stock_quant (session_id) WHERE session_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_categ_id_idx 
    ON stock_quant (categ_id) WHERE categ_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_ore_session_idx 
    ON stock_quant (ore_id, session_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_color_idx 
    ON stock_quant (color) WHERE color IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_size_idx 
    ON stock_quant (size) WHERE size IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_prod_loc_qty_idx 
    ON stock_quant (product_id, location_id, quantity);

-- ============================================
-- Stock Move Line Indexes
-- ============================================
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_product_location_idx 
    ON stock_move_line (product_id, location_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_picking_product_idx 
    ON stock_move_line (picking_id, product_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_move_idx 
    ON stock_move_line (move_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_location_dest_idx 
    ON stock_move_line (location_id, location_dest_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_state_idx 
    ON stock_move_line (state);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_lot_idx 
    ON stock_move_line (lot_id) WHERE lot_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_date_product_idx 
    ON stock_move_line (date, product_id);

-- Custom fields indexes (from project_custom)
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_ore_id_idx 
    ON stock_move_line (ore_id) WHERE ore_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_session_id_idx 
    ON stock_move_line (session_id) WHERE session_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_categ_id_idx 
    ON stock_move_line (categ_id) WHERE categ_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_date_ore_idx 
    ON stock_move_line (date, ore_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_date_session_idx 
    ON stock_move_line (date, session_id);

-- ============================================
-- Stock Move Indexes
-- ============================================
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_product_location_idx 
    ON stock_move (product_id, location_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_product_dest_idx 
    ON stock_move (product_id, location_dest_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_state_idx 
    ON stock_move (state);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_date_idx 
    ON stock_move (date);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_picking_idx 
    ON stock_move (picking_id);

-- ============================================
-- Stock Picking Indexes
-- ============================================
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_picking_state_idx 
    ON stock_picking (state);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_picking_type_idx 
    ON stock_picking (picking_type_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_picking_scheduled_date_idx 
    ON stock_picking (scheduled_date);

-- ============================================
-- POS Order Indexes
-- ============================================
CREATE INDEX CONCURRENTLY IF NOT EXISTS pos_order_session_idx 
    ON pos_order (session_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS pos_order_state_idx 
    ON pos_order (state);

CREATE INDEX CONCURRENTLY IF NOT EXISTS pos_order_date_idx 
    ON pos_order (date_order);

CREATE INDEX CONCURRENTLY IF NOT EXISTS pos_order_partner_idx 
    ON pos_order (partner_id) WHERE partner_id IS NOT NULL;

-- ============================================
-- Account Move Indexes (for POS invoices)
-- ============================================
CREATE INDEX CONCURRENTLY IF NOT EXISTS account_move_state_idx 
    ON account_move (state);

CREATE INDEX CONCURRENTLY IF NOT EXISTS account_move_journal_idx 
    ON account_move (journal_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS account_move_date_idx 
    ON account_move (date);

-- ============================================
-- Run ANALYZE after creating indexes
-- ============================================
ANALYZE product_product;
ANALYZE product_template;
ANALYZE stock_quant;
ANALYZE stock_move;
ANALYZE stock_move_line;
ANALYZE stock_picking;
ANALYZE pos_order;
ANALYZE account_move;

-- ============================================
-- Show created indexes
-- ============================================
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND (
      tablename LIKE 'product_%' 
      OR tablename LIKE 'stock_%' 
      OR tablename LIKE 'pos_%'
  )
ORDER BY tablename, indexname;

