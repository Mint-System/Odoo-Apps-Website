# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Sale Extra Infos",
    "summary": """
        Handling extra fields in website.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["website_sale", "sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/blacklist_views.xml",
        "views/sale_menu_views.xml",
        "views/product_template_views.xml",
        "views/website_templates.xml",
        "views/res_partner_views.xml",
        "views/block_view.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "assets": {
        "web.assets_frontend": [
            "website_sale_extra_infos/static/src/js/extra_info_validation.js",
            "website_sale_extra_infos/static/src/js/one_product.js",
        ]
    },
}
