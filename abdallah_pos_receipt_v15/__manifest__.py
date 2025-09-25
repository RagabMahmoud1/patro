{
    'name': 'POS Receipt Custom',
    'summary': 'Using this module you can print Custom pos receipt with product',
    'description': """Using this module you can print Custom pos receipt""",
    "version": "14.1.1.1",
    'sequence': 1,
    'email': 'aabdallahmohammed33@gmail.com',
    'website':'00201015065979',
    'category': 'Point of Sale',
    'author': 'Abdallah Mohamed',
    'price': 16,
    'currency': 'EUR',
    'license': 'OPL-1',
    "live_test_url" : "",
    'depends': ['point_of_sale'],

    'assets': {
        'web.assets_backend': [
            "abdallah_pos_receipt_v15/static/src/js/QuantityOrderSummary.js",
            "abdallah_pos_receipt_v15/static/src/js/TotalQuantityReceipt.js",
            "abdallah_pos_receipt_v15/static/src/js/deliverymethod_button.js",
            "abdallah_pos_receipt_v15/static/src/js/models.js",

        ],
        'web.assets_qweb': [
            "abdallah_pos_receipt_v15/static/src/xml/templates.xml",
            "abdallah_pos_receipt_v15/static/src/xml/TotalQuantitySummary.xml",
            "abdallah_pos_receipt_v15/static/src/xml/TotalQuantityReceipt.xml",
            "abdallah_pos_receipt_v15/static/src/xml/pos_delivery_method.xml",
        ],
    },



    'data': [
        'views/product_view.xml'
        ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

