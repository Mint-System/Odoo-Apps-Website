import logging
import json
from odoo.http import route, request
from odoo.exceptions import ValidationError
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)

class WebsiteSaleFormCheck(WebsiteSale):
    @route('/shop/payment', type='http', auth='public', website=True, sitemap=False)
    def shop_payment(self, **post):
        redirect_url = request.session.pop('form_check_redirect', False)
        _logger.warning(f"redirect_url: {redirect_url}")

        if redirect_url:
            return request.redirect(redirect_url)

        return super().shop_payment(**post)

