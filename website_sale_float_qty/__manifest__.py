{
    "name": "Website Sale Float Qty",
    "summary": """
        Add possibility to order product with decimal quantities on the website.
    """,
    "author": "Mint System GmbH, Solvti Sp. z o.o., Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Website",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["website_sale"],
    "data": [
        "data/uom_data.xml",
        "views/uom_uom_views.xml",
        "views/product_views.xml",
        "views/templates.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/product_demo.xml"],
    "assets": {
        "web.assets_frontend": [
            "website_sale_float_qty/static/src/js/website_sale.js",
        ],
    },
}
