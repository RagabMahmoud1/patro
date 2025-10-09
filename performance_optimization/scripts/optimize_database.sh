#!/bin/bash
# Database Optimization Script for Odoo 15 with Large Product Catalogs
# This script optimizes PostgreSQL database performance

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DB_NAME="patro"
DB_USER="odoo"
PGPASSWORD="1"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Odoo Database Optimization Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if running as root or with sudo
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}Warning: Running as root. Consider running as postgres user.${NC}"
fi

# Export password for psql
export PGPASSWORD=$PGPASSWORD

echo -e "${YELLOW}Step 1: Creating Database Indexes...${NC}"

psql -U $DB_USER -d $DB_NAME <<EOF
-- Product indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS product_product_barcode_idx ON product_product(barcode);
CREATE INDEX CONCURRENTLY IF NOT EXISTS product_product_default_code_idx ON product_product(default_code);
CREATE INDEX CONCURRENTLY IF NOT EXISTS product_product_tmpl_active_idx ON product_product(product_tmpl_id, active);

-- Stock quant indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_prod_loc_idx ON stock_quant(product_id, location_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_loc_prod_idx ON stock_quant(location_id, product_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_company_idx ON stock_quant(company_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_qty_prod_idx ON stock_quant(quantity, product_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_lot_idx ON stock_quant(lot_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_quant_reserved_qty_idx ON stock_quant(reserved_quantity, location_id);

-- Stock move line indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_prod_loc_idx ON stock_move_line(product_id, location_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_pick_prod_idx ON stock_move_line(picking_id, product_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_move_idx ON stock_move_line(move_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_loc_dest_idx ON stock_move_line(location_id, location_dest_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_state_idx ON stock_move_line(state);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_lot_idx ON stock_move_line(lot_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_line_date_prod_idx ON stock_move_line(date, product_id);

-- Stock move indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_prod_loc_idx ON stock_move(product_id, location_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_prod_dest_idx ON stock_move(product_id, location_dest_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_state_idx ON stock_move(state);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_date_idx ON stock_move(date);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_move_picking_idx ON stock_move(picking_id);

-- POS indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS pos_order_session_idx ON pos_order(session_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS pos_order_state_idx ON pos_order(state);
CREATE INDEX CONCURRENTLY IF NOT EXISTS pos_order_date_idx ON pos_order(date_order);
CREATE INDEX CONCURRENTLY IF NOT EXISTS pos_order_partner_idx ON pos_order(partner_id);

-- Stock picking indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_picking_state_idx ON stock_picking(state);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_picking_type_idx ON stock_picking(picking_type_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS stock_picking_scheduled_date_idx ON stock_picking(scheduled_date);

\echo 'Indexes created successfully!'
EOF

echo -e "${GREEN}✓ Indexes created${NC}"
echo ""

echo -e "${YELLOW}Step 2: Analyzing Tables...${NC}"

psql -U $DB_USER -d $DB_NAME <<EOF
ANALYZE product_product;
ANALYZE product_template;
ANALYZE stock_quant;
ANALYZE stock_move;
ANALYZE stock_move_line;
ANALYZE stock_picking;
ANALYZE pos_order;
ANALYZE pos_order_line;

\echo 'Tables analyzed successfully!'
EOF

echo -e "${GREEN}✓ Tables analyzed${NC}"
echo ""

echo -e "${YELLOW}Step 3: Vacuuming Important Tables...${NC}"

psql -U $DB_USER -d $DB_NAME <<EOF
VACUUM ANALYZE product_product;
VACUUM ANALYZE product_template;
VACUUM ANALYZE stock_quant;
VACUUM ANALYZE stock_move;
VACUUM ANALYZE stock_move_line;
VACUUM ANALYZE stock_picking;
VACUUM ANALYZE pos_order;

\echo 'Tables vacuumed successfully!'
EOF

echo -e "${GREEN}✓ Tables vacuumed${NC}"
echo ""

echo -e "${YELLOW}Step 4: Checking Database Statistics...${NC}"

psql -U $DB_USER -d $DB_NAME <<EOF
-- Show table sizes
SELECT 
    schemaname as schema,
    tablename as table,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN ('product_product', 'stock_quant', 'stock_move', 'stock_move_line', 'pos_order')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Show index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND tablename IN ('product_product', 'stock_quant', 'stock_move_line')
ORDER BY idx_scan DESC
LIMIT 20;
EOF

echo -e "${GREEN}✓ Database statistics displayed${NC}"
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Optimization Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Restart Odoo server: sudo systemctl restart odoo"
echo "2. Test POS session opening performance"
echo "3. Test stock report generation"
echo "4. Monitor server logs for any issues"
echo ""
echo -e "${YELLOW}Recommended PostgreSQL Configuration:${NC}"
echo "Add to /etc/postgresql/*/main/postgresql.conf:"
echo "  shared_buffers = 2GB"
echo "  effective_cache_size = 6GB"
echo "  maintenance_work_mem = 512MB"
echo "  checkpoint_completion_target = 0.9"
echo "  wal_buffers = 16MB"
echo "  default_statistics_target = 100"
echo "  random_page_cost = 1.1"
echo "  effective_io_concurrency = 200"
echo "  work_mem = 10MB"
echo "  min_wal_size = 1GB"
echo "  max_wal_size = 4GB"
echo ""
echo "Then restart PostgreSQL: sudo systemctl restart postgresql"
echo ""

