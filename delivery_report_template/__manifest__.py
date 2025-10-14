# -*- coding: utf-8 -*-
{
    'name': 'Delivery Report - Product Template View',
    'version': '15.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Show Product Template instead of Product Variant in Delivery Report',
    'description': """
Delivery Report Customization
==============================

This module provides a custom delivery report that shows:
* Product Template name instead of Product Variant
* Groups products by template for cleaner delivery notes
* Arabic-friendly layout

Perfect for businesses that want simplified delivery documents.
    """,
    'author': 'Delivery Report Team',
    'depends': ['stock'],
    'data': [
        'reports/delivery_report.xml',
        'reports/delivery_report_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

