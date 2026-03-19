# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Auth Signup Firstname",
    "summary": """
        Allows to log in with first name and last name on the website.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["auth_signup", "partner_firstname"],
    "data": [
        "views/auth_signup_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    
}
