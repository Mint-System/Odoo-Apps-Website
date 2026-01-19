# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Sale Permit Extra Info",
    "summary": """
        Adds extra webshop page and data validation and processing to permit sale workflow.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["website_sale", "sale_order_permit", "calendar_public_holiday"],
    "data": [
       "views/website_templates.xml",
       "views/website_products.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    'assets': {
        'web.assets_frontend': [
            "website_sale_permit_extra_info/static/src/js/extra_info_validation.js",
            "website_sale_permit_extra_info/static/src/js/one_product.js",
            "website_sale_permit_extra_info/static/src/js/show_products.js",
        ]
    }
}
