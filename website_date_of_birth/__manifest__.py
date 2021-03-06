{
    "name": "Website Date of Birth",
    "summary": """
        Adds date of birth field to partner and website checkout form.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Website",
    "version": "14.0.1.0.1",
    "license": "AGPL-3",
    "depends": ["base", "website"],
    "data": [
        "views/base_view_partner_form.xml",
        "views/website_sale_address.xml",
        "data/data.xml",
    ],
    "installable": True,
    "application": False,
    "images": ["images/screen.png"],
}
