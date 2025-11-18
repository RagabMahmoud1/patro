# -*- coding: utf-8 -*-
{
    'name': "project_custom",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'point_of_sale','stock','account','mrp','purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/pos.xml',
        'views/partner.xml',
        'views/settings.xml',
        'views/payment.xml',
        'views/user.xml',
        'views/stock.xml',
        'views/report_pos_order.xml',
        'views/price.xml',
        'wizards/wiz.xml',
        'wizards/expenses.xml',
        'wizards/sales.xml',
    ],

    'assets': {
        'point_of_sale.assets': [
            'project_custom/static/src/js/pos.js',
            'project_custom/static/src/js/barcode.js',
            'project_custom/static/src/js/SelectionPopup2.js',
            'project_custom/static/src/js/price_list.js',
            'project_custom/static/src/js/cash.js',
            'project_custom/static/src/js/cash2.js',
            'project_custom/static/src/js/TicketScreen.js',
            'project_custom/static/src/js/sale.js',
            'project_custom/static/src/js/hr_button.js',
            'project_custom/static/src/js/hr_pop.js',
        ],
        'web.assets_qweb': [
            'project_custom/static/src/xml/**/*',
        ],
    },


}
