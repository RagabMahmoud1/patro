# -*- coding: utf-8 -*-
{
    'name': "Performance Optimization for Large Product Catalogs",
    'summary': "Database indexes and performance improvements for 28K+ product variants",
    'description': """
Performance Optimization Module
================================

This module provides performance optimizations for Odoo 15 installations
with large product catalogs (28,000+ product variants).

Key Features:
-------------
* Database indexes on critical tables (product.product, stock.quant, stock.move.line)
* Optimized stock report queries
* POS session opening optimization
* Computed field performance improvements
* Database maintenance utilities

Optimizations:
--------------
1. Adds indexes on product fields (barcode, default_code, ore_id, session_id)
2. Adds indexes on stock.quant (product_id, location_id, ore_id, session_id)
3. Adds indexes on stock.move.line (product_id, location_id, picking_id)
4. Optimizes POS product loading with smart filtering
5. Reduces N+1 queries in stock reports

Installation:
-------------
1. Install this module
2. Run the database optimization script
3. Restart Odoo server
    """,
    'author': "Odoo Performance Team",
    'website': "https://www.odoo.com",
    'category': 'Technical',
    'version': '15.0.1.0.0',
    'depends': [
        'base',
        'product',
        'stock',
        'point_of_sale',
        'project_custom',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/db_index_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

