from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSalePricelistPersist(WebsiteSale):
    @http.route(
        ['/shop/change_pricelist/<model("product.pricelist"):pricelist>'],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def pricelist_change(self, pricelist, **post):
        response = super().pricelist_change(pricelist, **post)

        # Store chosen pricelist in session
        request.session["chosen_pricelist_id"] = pricelist.id

        # Persist for logged-in users
        user = request.env.user
        if not user._is_public():
            user.partner_id.sudo().write({"property_product_pricelist": pricelist.id})

        return response
