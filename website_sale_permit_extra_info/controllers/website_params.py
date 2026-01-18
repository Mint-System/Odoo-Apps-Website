import logging

from datetime import timedelta

from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsiteParamController(http.Controller):


    def get_blacklisted_dates(self):
        """Return all holiday dates from today onwards."""

        today = fields.Date.today()
        company = request.website.company_id

        leaves = request.env['resource.calendar.leaves'].sudo().search([
            ('date_to', '>=', today),
            ('company_id', 'in', [company.id, False]),
        ])
        _logger.warning(f"###########  leaves: {leaves}")

        blacklisted = set()

        for leave in leaves:
            start = max(leave.date_from.date(), today)
            end = leave.date_to.date()

            current = start
            while current <= end:
                blacklisted.add(current.isoformat())
                current += timedelta(days=1)

        return sorted(blacklisted)


    def get_photo_need(self, duration):
        if duration == 'year':
            return True
        return False


    @http.route("/website/get_params", type="json", auth="public", csrf=False, website=True)
    def get_params(self, **kwargs):
        order_id = request.session.get("sale_order_id")
        # order = request.website.sale_get_order()
        # blacklisted_dates = request.env['blacklist.date'].sudo().search([]).mapped('date')
        blacklisted_dates = self.get_blacklisted_dates()
        _logger.warning(f"blacklisted dates: {blacklisted_dates}")
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
                needs_photo = self.get_photo_need(product.duration)

            patent_lines_of_partner = request.env["sale.order.line"].sudo().search([
                ("order_partner_id", "=", partner.id),
                ('product_id.duration', '!=', False),
            ])

            _logger.warning(f"patent lines: {patent_lines_of_partner}")

            for line in patent_lines_of_partner:
                year = line.date_from.year
                duration = line.product_id.duration
                _logger.warning(f"############ duration: {duration}")

                if duration:
                    if year not in patents_by_year:
                        patents_by_year[year] = {"day": 0, "week": 0, "year": 0}

                    patents_by_year[year][duration] += 1

        params = {
            "blacklisted_dates": blacklisted_dates,
            "needs_photo": needs_photo,
            "min_age": min_age,
            "future_only": future_only,
            "patents_by_year": patents_by_year,
            "max_day": 5,
            "max_week": 1,
            "max_year": 1,
            "duration": duration
        }
        _logger.warning(f"params: {params}")
        return params



