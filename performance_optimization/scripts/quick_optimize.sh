#!/bin/bash
# ============================================
# Quick Database Optimization Script
# Run this to add all performance indexes
# ============================================

# Configuration - CHANGE THESE VALUES
DB_NAME="${1:-patro}"
DB_USER="${2:-odoo}"
DB_PASS="${3:-1}"

echo "============================================"
echo "Quick Performance Optimization"
echo "Database: $DB_NAME"
echo "============================================"

# Export password
export PGPASSWORD=$DB_PASS

# Run the full SQL script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "Creating indexes..."
psql -U $DB_USER -d $DB_NAME -f "$SCRIPT_DIR/create_all_indexes.sql"

echo ""
echo "============================================"
echo "Done! Indexes created."
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Restart Odoo: sudo systemctl restart odoo"
echo "2. Test the performance"
echo ""

