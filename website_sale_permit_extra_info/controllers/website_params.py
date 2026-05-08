import logging

from odoo import fields, http
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsiteParamController(http.Controller):
    def get_blacklisted_dates(self):
        """Return all publich holiday dates from today onwards."""

        _logger.warning("get_blacklisted_dates called")

        today = fields.Date.today()
        company = request.website.company_id

        # does not work, why?
        # country = company.country_id
        country = "Schweiz"
        _logger.warning(f"Company Country {country}")

        calendars = (
            request.env["calendar.public.holiday"]
            .sudo()
            .search(
                [
                    ("year", ">=", today.year),
                    ("country_id.name", "=", country),
                ]
            )
        )
        _logger.warning(f"calendars: {calendars}")

        dates = calendars.mapped("line_ids.date")

        return sorted(d for d in dates if d >= today)

    def get_photo_need(self, duration):
        if duration in ["year", "week", "day"]:
            return True
        return False

    @http.route("/website/get_params", type="json", auth="user", csrf=False, website=True)
    def get_params(self, **kwargs):
        order_id = request.session.get("sale_order_id")
        if not order_id and request.env.user._is_public():
            return request.redirect('/web/login')
        
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
                product_duration = product.duration

            if not partner.is_public:
                domain = [
                    ("order_partner_id.id", "=", partner.id),
                    ("product_id.duration", "!=", False),
                ]
            else:
                domain = [
                    ("order_partner_id.email", "=", partner.email),
                    ("product_id.duration", "!=", False),
                ]

            patent_lines_of_partner = request.env["sale.order.line"].sudo().search(domain)

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
            "has_existing_photo": bool(partner.image_1920),
            "min_age": min_age,
            "future_only": future_only,
            "patents_by_year": patents_by_year,
            "max_day": 5,
            "max_week": 1,
            "max_year": 1,
            "duration": product_duration,
        }
        _logger.warning(f"params: {params}")
        return params
