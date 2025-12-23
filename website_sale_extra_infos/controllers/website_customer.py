from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCustomerBlacklist(WebsiteSale):
    def _is_customer_blacklisted(self, vals):
        blacklist = request.env["blacklist.customer"].sudo().search([])

        for rule in blacklist:
            # Email block
            if rule.email and vals.get("email") and vals["email"].lower() == rule.email.lower():
                # return rule.message or "Email ist gesperrt. Bitte kontaktieren Sie die Geschäftsstelle."
                return True

            # Street block (contains)
            if rule.street and vals.get("street") and rule.street.lower() in vals["street"].lower():
                # return rule.message or "Adresse ist gesperrt. Bitte kontaktieren Sie die Geschäftsstelle."
                return True

            # ZIP
            if rule.zip and vals.get("zip") and vals["zip"] == rule.zip:
                # return rule.message or "PLZ ist gesperrt. Bitte kontaktieren Sie die Geschäftsstelle."
                return True

        return False

    def shop_address_submit(self, **form_data):
        """
        Override only enough to block blacklisted users
        BEFORE Odoo tries to create or update a partner.
        """
        # Convert form data to res.partner fields
        address_values, extra_form_data = self._parse_form_data(form_data)

        # === CHECK BLACKLIST IMMEDIATELY ===
        blacklisted = self._is_customer_blacklisted(address_values)
        # if blacklist_msg:
        #     return request.make_json_response({
        #         "invalid_fields": ["email", "street", "zip"],
        #         "messages": [blacklist_msg],
        #     })
        # if blacklist_msg:
        #     # Show ONE global error message to the user
        #     return request.make_json_response({
        #         "messages": ["Please contact the bureau."]
        #     })

        if blacklisted:
            return request.make_json_response({"redirectUrl": "/shop/blocked"})

        # If ok, continue normal Odoo flow
        return super().shop_address_submit(**form_data)

    @http.route("/shop/blocked", type="http", auth="public", website=True)
    def shop_blocked(self):
        # Clear the shopping cart
        order = request.website.sale_get_order()
        if order and order.order_line:
            order.order_line.unlink()
            request.website.sale_reset()

        return request.render("website_sale_extra_infos.shop_blocked_page")
