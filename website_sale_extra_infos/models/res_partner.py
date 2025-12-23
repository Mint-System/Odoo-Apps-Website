import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    birthdate = fields.Date(string="Birthdate", required=False)

    patent_ids = fields.One2many(
        comodel_name="sale.order.line",
        inverse_name="partner_id",
        string="Patents",
        domain=[("is_patent", "=", True)],
    )

    patents_day_count = fields.Integer(compute="_compute_patent_stats", string="Day Patents (this year)")
    patents_week_count = fields.Integer(compute="_compute_patent_stats", string="Week Patents (this year)")
    patents_year_count = fields.Integer(compute="_compute_patent_stats", string="Year Patents (this year)")
    image_released = fields.Boolean(string="Image released", default=False)

    @api.depends("patent_ids", "patent_ids.date_from")
    def _compute_patent_stats(self):
        for partner in self:
            day = week = year = 0
            year_now = fields.Date.today().year

            for line in partner.patent_ids:
                if line.date_from and line.date_from.year == year_now:
                    if line.duration == "day":
                        day += 1
                    elif line.duration == "week":
                        week += 1
                    elif line.duration == "year":
                        year += 1

            partner.patents_day_count = day
            partner.patents_week_count = week
            partner.patents_year_count = year
