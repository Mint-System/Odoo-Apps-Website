import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class WebsiteBlacklistController(http.Controller):

    @http.route("/website/blacklist_dates", type="json", auth="public", csrf=False)
    def blacklist_dates(self):
        dates = request.env['blacklist.date'].sudo().search([]).mapped('date')
        _logger.warning(f"dates: {dates}")
        return dates



