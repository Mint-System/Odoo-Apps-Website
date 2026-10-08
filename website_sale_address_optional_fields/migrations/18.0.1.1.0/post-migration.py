from odoo import SUPERUSER_ID, api

from odoo.addons.website_sale_address_optional_fields.hooks import post_init_hook


def migrate(cr, version):
    """Keep the previously hardcoded optional fields (name, email, phone)."""
    post_init_hook(api.Environment(cr, SUPERUSER_ID, {}))
