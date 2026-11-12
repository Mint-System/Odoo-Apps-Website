# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Sale Select Address Type",
    "summary": """
        Add is-company field to address forms.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["website_sale"],
    "data": [
        "views/address.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "assets": {
        "web.assets_frontend": [
            "website_sale_select_address_type/static/src/scss/address_type.scss",
        ],
    },
    "images": ["images/screen.png"],
}
