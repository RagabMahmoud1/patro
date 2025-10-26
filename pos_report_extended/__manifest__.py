# -*- coding: utf-8 -*-
{
    'name': 'POS Report Extended',
    'version': '15.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Add Cost and On Hand to POS Report',
    'description': """
POS Report Extended
===================

Adds additional fields to POS Order Report:
* Product Cost (standard_price)
* Quantity on Hand (qty_available)
    """,
    'author': 'POS Report Team',
    'depends': ['point_of_sale', 'stock'],
    'data': [
        'views/pos_order_report_views.xml',
        'views/stock_quant_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

