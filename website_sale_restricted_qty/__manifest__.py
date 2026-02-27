# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Sale Restricted Qty",
    "summary": """
        Set minimum order quantity for product variants.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale_restricted_qty", "website_sale"],
    "data": [
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_restricted_qty/static/src/js/website_sale_min_order.js"
        ]
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
