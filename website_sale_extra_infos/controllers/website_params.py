import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class WebsiteParamController(http.Controller):

    @http.route("/website/get_params", type="json", auth="public", csrf=False)
    def get_params(self, **kwargs):
        order_id = request.session.get("sale_order_id")
        # order = request.website.sale_get_order()
        blacklisted_dates = request.env['blacklist.date'].sudo().search([]).mapped('date')
        needs_photo = False
        min_age = 14 
        future_only = True
        
        if order_id:
            order = request.env["sale.order"].sudo().browse(order_id)
            if order.order_line:
                product = order.order_line[0].product_id
                needs_photo = bool(product.needs_photo)
            else:
                needs_photo = False

        return {
            "blacklisted_dates": blacklisted_dates,
            "needs_photo": needs_photo,
            "min_age": min_age,
            "future_only": future_only,
        }



