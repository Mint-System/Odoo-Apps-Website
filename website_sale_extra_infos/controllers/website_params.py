import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsiteParamController(http.Controller):
    @http.route("/website/get_params", type="json", auth="public", csrf=False)
    def get_params(self, **kwargs):
        order_id = request.session.get("sale_order_id")
        # order = request.website.sale_get_order()
        blacklisted_dates = request.env["blacklist.date"].sudo().search([]).mapped("date")
        needs_photo = False
        min_age = 14
        future_only = True
        day_patents = 0
        week_patents = 0
        year_patents = 0
        patents_by_year = {}
        duration = ""

        if order_id:
            order = request.env["sale.order"].sudo().browse(order_id)
            partner = order.partner_id if order else request.env.user.partner_id
            if order.order_line:
                product = order.order_line[0].product_id
                needs_photo = bool(product.needs_photo)

            patent_lines = (
                request.env["sale.order.line"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner.id),
                        ("is_patent", "=", True),
                    ]
                )
            )
            _logger.warning(f"patent lines: {patent_lines}")

            for line in patent_lines:
                year = line.date_from.year
                duration = line.product_id.duration
                _logger.warning(f"############ duration: {duration}")

                if duration:
                    if year not in patents_by_year:
                        patents_by_year[year] = {"day": 0, "week": 0, "year": 0}

                    patents_by_year[year][duration] += 1

        return {
            "blacklisted_dates": blacklisted_dates,
            "needs_photo": needs_photo,
            "min_age": min_age,
            "future_only": future_only,
            "patents_by_year": patents_by_year,
            "max_day": 5,
            "max_week": 1,
            "max_year": 1,
            "duration": duration,
        }
