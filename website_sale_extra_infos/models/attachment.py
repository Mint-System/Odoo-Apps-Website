from odoo import models, fields

class Attachment(models.Model):
    _inherit = "ir.attachment"

    usage_type = fields.Selection([
        ("passport_photo", "Passport Photo"),
    ], string="Attachment Type")
