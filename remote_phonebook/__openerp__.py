# -*- coding: utf-8 -*-
{
    'name': "Remote Phonebook",

    'summary': """
        Basic Handler for remote phonebooks.""",

    'description': """
        Does allow you to create a special URL with an access tokken, where your phonebook can get access read only from remote.
        This is useful for example to get your contacts into the phonebook of your local desk phone.
        This is the basic module, you do need also a model specific module depending on the desk phone you are using.
    """,

    'author': "Callino",
    'website': "http://www.callino.at",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'CRM',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm'],

    # always loaded
    'data': [
        'views/remote_phonebook.xml',
        'menu.xml',
        'security/ir.model.access.csv',
    ],

    'qweb': [],
    # only loaded in demonstration mode
    'demo': [
    ],
    "external_dependencies": {
    },
}