{
    'name': 'Product Vendor & Model',
    'version': '15.0',
    'summary': 'Add vendor and model fields to products and show in sale orders',
    'category': 'Sales',
    'depends': ['sale', 'product','point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
}