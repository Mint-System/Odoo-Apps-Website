import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

from .config import DURATION_SELECTION


class ProductTemplate(models.Model):
    _inherit = "product.template"

    duration = fields.Selection(selection=DURATION_SELECTION)
    needs_photo = fields.Boolean(string="Needs Passport Photo", default=False)
    is_patent = fields.Boolean(compute="_compute_is_patent", store=True)

    @api.depends("duration")
    def _compute_is_patent(self):
        for product in self:
            product.is_patent = False
            if product.duration:
                product.is_patent = True
