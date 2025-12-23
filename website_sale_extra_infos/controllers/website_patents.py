import json
import logging

from odoo import fields, http
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsitePatentController(http.Controller):
    @http.route("/website/patent/check_limit", type="http", auth="public", methods=["GET", "POST"], csrf=False)
    def check_patent_limit(self, date_from=None, **post):
        """Return number of already used patents for the given partner/year/duration"""
        # data = request.httprequest.get_json() or {}
        # _logger.warning(f"#### {data}")
        # date_from = data.get("date_from")

        try:
            date_from = post.get("date_from") or date_from

            if request.httprequest.method == "POST":
                try:
                    data = request.httprequest.get_json() or {}
                    date_from = data.get("date_from") or post.get("date_from") or date_from
                except Exception as e:
                    _logger.error(f"Error parsing JSON data: {e}")

            if not date_from:
                return {"error": "No date_from provided"}

            year = fields.Date.from_string(date_from).year

            order_id = request.session.get("sale_order_id")

            limits = {
                "day": 5,
                "week": 1,
                "year": 1,
            }

            limit = 9999
            used_count = 0

            if order_id:
                order = request.env["sale.order"].sudo().browse(order_id)
                partner = order.partner_id

                if order.order_line:
                    product = order.order_line[0].product_id
                    duration = product.duration
                    limit = limits.get(duration, 9999)

                    used_count = (
                        request.env["patent.history"]
                        .sudo()
                        .search_count(
                            [
                                ("partner_id", "=", int(partner.id)),
                                ("duration", "=", duration),
                                ("year", "=", year),
                            ]
                        )
                    )

            # return {
            #     "result": {
            #         "used": used_count,
            #         "limit": limit,
            #         "allowed": used_count < limit
            #     }
            # }

            # return {
            #     "used": used_count,
            #     "limit": limit,
            #     "allowed": used_count < limit
            # }
            result = {"used": used_count, "limit": limit, "allowed": used_count < limit}

            _logger.warning(f"##### {result}")

            return request.make_response(json.dumps(result), headers={"Content-Type": "application/json"})

        except Exception as e:
            _logger.error(f"Error in check_patent_limit: {e}")
            # Return a safe default to not block the user
            error_result = {
                "used": 0,
                "limit": 9999,
                "allowed": True,  # Default to allowing if there's an error
                "error": str(e),
            }
            return request.make_response(json.dumps(error_result), headers={"Content-Type": "application/json"})
