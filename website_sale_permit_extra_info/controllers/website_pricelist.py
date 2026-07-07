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
        website = request.env["website"].get_current_website()
        previous_pl_id = website.pricelist_id.id if website.pricelist_id else None
        response = super().pricelist_change(pricelist, **post)

        # Store chosen pricelist in session
        request.session["chosen_pricelist_id"] = pricelist.id

        # Persist for logged-in users
        user = request.env.user
        if not user._is_public():
            user.partner_id.sudo().write({"property_product_pricelist": pricelist.id})

        # if the pricelist actually changed clear cart
        if previous_pl_id and previous_pl_id != pricelist.id:
            order_sudo = website.sale_get_order()
            if order_sudo and order_sudo.order_line:
                order_sudo.order_line.unlink()
                request.session["cart_cleared_notice"] = True
                return request.redirect("/shop/cart")

        return response
