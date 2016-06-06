# -*- coding: utf-8 -*-
{
    'name': "Remote Phonebook for Yealink",

    'summary': """Does add support for Yealink phones""",

    'description': """
        Does add export format for yealink Phones
    """,

    'author': "Callino",
    'website': "http://www.callino.at/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'CRM',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm', 'remote_phonebook'],

    # always loaded
    'data': [
    ],

    'qweb': [],
    # only loaded in demonstration mode
    'demo': [
    ],
    "external_dependencies": {
    },
}