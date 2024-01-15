{
    "name": "Website Date of Birth",
    "summary": """
        Adds date of birth field to partner and website checkout form.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Website",
    "version": "15.0.1.1.0",
    "license": "AGPL-3",
    "depends": ["website_sale"],
    "data": [
        "views/res_partner.xml",
        "views/website_sale_address.xml",
        "data/data.xml",
    ],
    "installable": True,
    "application": False,
    "images": ["images/screen.png"],
}
