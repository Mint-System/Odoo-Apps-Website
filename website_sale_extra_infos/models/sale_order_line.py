import logging
from datetime import timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

from .config import DURATION_SELECTION, REGION_SELECTION


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_from = fields.Date(
        string="Start Date", required=True, help="Start Date of Patent", default=fields.Date.today()
    )

    date_to = fields.Date(compute="_compute_date_to")

    birthdate = fields.Date(
        compute="_compute_birthdate",
    )

    region = fields.Selection(
        string="Region",
        selection=REGION_SELECTION,
        default="none",
    )

    liability_insurance = fields.Boolean(string="Liability Insurance", default=False)

    code_of_honour = fields.Boolean(string="Code of Honour", default=False)

    strahlner_ordinance = fields.Boolean(string="Strahlner Ordinance", default=False)

    minimum_age = fields.Boolean(string="Minimum Age", default=False)

    duration = fields.Selection(
        selection=DURATION_SELECTION,
        compute="_compute_duration",
        store=False,
        readonly=True,
    )

    partner_id = fields.Many2one(
        related="order_id.partner_id",
        store=True,
    )

    is_patent = fields.Boolean(
        string="is patent",
        related="product_id.is_patent",
        store=True,
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
            if line.date_from and line.product_id.duration in duration_map.keys():
                line.date_to = line.date_from + timedelta(**duration_map[duration])
            else:
                line.date_to = line.date_from

    def _compute_birthdate(self):
        for line in self:
            if line.order_id and line.order_id.partner_id:
                line.birthdate = line.order_id.partner_id.birthdate
            else:
                line.birthdate = False

    def _compute_duration(self):
        for line in self:
            line.duration = line.product_id.duration
