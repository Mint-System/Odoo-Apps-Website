import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    duration = fields.Selection([("day", "Day"), ("week", "Week"), ("year", "Year")])
    needs_photo = fields.Boolean(
        string="Nees Passport Photo",
        default=False
    )



