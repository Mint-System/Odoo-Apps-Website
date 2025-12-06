import logging
from datetime import timedelta

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

from .config import REGION_SELECTION


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_from = fields.Date(
        string='Start Date', required=True,
        help='Start Date of Patent',
        default=fields.Date.today()
        )

    date_to = fields.Date(
        compute="_compute_date_to")

    birthdate = fields.Date(
        compute="_compute_birthdate",
    )


    region = fields.Selection(
        string="Region",
        selection = REGION_SELECTION,
        default="none",
        )

    @api.depends("date_from")
    def _compute_date_to(self):
        duration_translator = {
            'year': 'years=1',
            'day': 'days=1',
            'week': 'week=1'
        }
        for line in self:
            duration = line.product_id.duration
            if line.date_from and line.product_id.duration in duration_translator.keys():
                line.date_to = self.date_from + timedelta(duration_translator[duration]) 
            else:
                line.date_to = line.date_from

    def _compute_birthdate(self):
        self.birthdate = self.order_id.res_partner_birthdate

