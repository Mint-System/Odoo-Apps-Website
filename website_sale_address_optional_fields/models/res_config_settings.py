from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    address_optional_field_ids = fields.Many2many(
        related="website_id.address_optional_field_ids",
        readonly=False,
    )
