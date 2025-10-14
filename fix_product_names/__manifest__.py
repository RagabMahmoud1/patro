# -*- coding: utf-8 -*-
{
    'name': 'Fix Product Names',
    'version': '15.0.1.0.0',
    'summary': 'Fix product names to match default_code',
    'description': """
        This module fixes product names that contain incorrect reference numbers.
        It ensures that the product name starts with the correct default_code.
    """,
    'author': 'Odoo Developer',
    'category': 'Inventory',
    'depends': ['product', 'stock'],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}

