# -*- coding: utf-8 -*-
{
    'name': 'Stock Report Optimization',
    'version': '15.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Optimize stock quantity report for large product catalogs (28,000+ products)',
    'description': """
This module optimizes the stock quantity report for large product catalogs.

Features:
* Adds pagination to limit loaded products
* Uses direct SQL queries for better performance
* Implements lazy loading strategy
* Filters products with zero stock by default
* Adds search and filter options

Perfect for systems with 28,000+ product variants.
    """,
    'author': 'Stock Performance Team',
    'depends': ['stock', 'web'],
    'data': [
        'views/stock_quant_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

