# -*- coding: utf-8 -*-
# Sinergia


{
    "name" : "POS Control de stock Super Barato",
    "version" : "14.0.0.6",
    "category" : "Point of Sale",
    "depends" : ['base','sale_management','stock','point_of_sale'],
    "author": "Sinergia",
    'summary': 'Control de stock POS',
    'price': 600,
    'currency': "MXN",
    "description": """
    Se bloquea la venta en negativo
    """,
    "website" : "https://www.sinergia-e.com",
    "data": [
        # 'views/assets.xml',
        'views/custom_pos_config_view.xml',
    ],


    'assets': {
        'point_of_sale.assets': [
            'sinergia_stock/static/src/js/Chrome.js',
            'sinergia_stock/static/src/js/SyncStock.js',
            'sinergia_stock/static/src/js/models.js',
            'sinergia_stock/static/src/js/Screens/ProductScreen.js',
            'sinergia_stock/static/src/js/Screens/ProductsWidget.js',
            'sinergia_stock/static/src/js/Screens/ReceiptScreen.js',
        ],
        'web.assets_qweb': [
            'sinergia_stock/static/src/xml/**/*',
        ],
    },
    "auto_install": False,
    "installable": True,
}
