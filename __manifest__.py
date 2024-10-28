# -*- coding: utf-8 -*-
{
    'name': 'GUERRABIFintech',
    'version': '2.0',
    'category': 'Tests',
    'description': """A BASIC FINTECH MODULE.""",
    'depends': ['base', 'web','stock'],
    'installable': True,
    'auto_install': False,
    'data': [
        'security.xml',
        'ir.model.access.csv',
        'views.xml',
        'reports/credit_report.xml',
        
    ],
}
