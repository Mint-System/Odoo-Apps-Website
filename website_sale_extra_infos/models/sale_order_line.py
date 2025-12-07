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

    liability_insurance = fields.Boolean(
        string="Liability Insurance",
        default=False
        )

    code_of_honour =  fields.Boolean(
        string="Code of Honour",
        default=False
    )

    strahlner_ordinance =  fields.Boolean(
        string="Strahlner Ordinance",
        default=False
    )

    minimum_age =  fields.Boolean(
        string="Minimum Age",
        default=False
    )

    
    @api.depends("date_from")
    def _compute_date_to(self):
        duration_map = {
            "year": {"days": 365},
            "day": {"days": 1},
            "week": {"weeks": 1},
        }
        for line in self:
            duration = line.product_id.duration
            _logger.warning(f"duration: {duration}")
            _logger.warning(f"shift: {duration_map[duration]}")
            if line.date_from and line.product_id.duration in duration_map.keys():
               line.date_to = self.date_from + timedelta(**duration_map[duration])
            else:
                line.date_to = line.date_from

    def _compute_birthdate(self):
        self.birthdate = self.order_id.res_partner_birthdate



