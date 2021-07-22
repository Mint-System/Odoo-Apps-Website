# -*- coding: utf-8 -*-
{
    'name': "Website Product Description",

    'summary': """
        Add separate description field to website product view.
    """,

    'author': "Mint System GmbH",
    'website': "https://www.mint-system.ch",
    'category': 'Accounting',
    'version': '14.0.1.0.1',

    'depends': ['website_sale'],

    'data': [
        'views/product_product_normal_form_view.xml',
        'views/product_product_template_only_form_view.xml',
        'views/website_sale_product.xml',
    ],

    'installable': True,
    'application': False,
}