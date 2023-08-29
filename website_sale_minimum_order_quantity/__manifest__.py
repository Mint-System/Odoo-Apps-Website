{
    "name": "Website Sale Minium Order Quantity",
    "summary": """
        Set minimum order quantity for product variants.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Website",
    "version": "16.0.1.0.3",
    "license": "AGPL-3",
    "depends": ["website_sale", "sale_product_configurator"],
    "data": ["views/product.xml", "views/templates.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "assets": {
        "web.assets_frontend": [
            "website_sale_minimum_order_quantity/static/src/js/website_sale_min_order.js"
        ]
    },
}
