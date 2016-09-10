# -*- coding: utf-8 -*-
{
    'name': "Deep Menu on Website",

    'summary': """
        Get more than deepth=2 on website menu
    """,

    'description': """
    Does replace original EditMenu dialog with a copy which does support more than deepth=2
    """,

    'author': "Callino",
    'website': "http://www.callino.at",

    'category': 'Website',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],

    # always loaded
    'data': [
        'views/assets.xml',
        'views/deepmenu.xml',
    ],

    'qweb': [

    ],

    'demo': [

    ],

    "external_dependencies": {
    },
}