# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Form Check",
    "summary": """
        Create form checks that redirect users on a match.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["website_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/website_views.xml",
        "views/website_form_check_views.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
