{
    'name': 'Variant Auto Fix',
    'summary': 'Automatically fix POS variant grouping issues',
    'description': 'Auto-fix Undefined grouping in POS by resetting variant attributes while preserving all data',
    'depends': ['product'],
    'data': [
        'data/cron_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}