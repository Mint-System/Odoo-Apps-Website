# -*- coding: utf-8 -*-
{
    'name': "Website Sale Default Country",

    'summary': """
        Set switzerland as the default country in the website sale address from.
    """,

    'author': "Mint System GmbH",
    'website': "https://www.mint-system.ch",
    'category': 'Website',
    'version': '14.0.1.0.1',

    'depends': [
        'base',
        'website'
    ],

    'data': [
        'views/templates.xml',
    ],

    'installable': True,
    'application': False,
}