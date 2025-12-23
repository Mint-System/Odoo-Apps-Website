from odoo import fields, models


class Attachment(models.Model):
    _inherit = "ir.attachment"

    usage_type = fields.Selection(
        [
            ("passport_photo", "Passport Photo"),
        ],
        string="Attachment Type",
    )
