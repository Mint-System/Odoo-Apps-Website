import logging

from odoo.exceptions import UserError
from odoo.http import request

from odoo.addons.web.controllers.home import SIGN_UP_REQUEST_PARAMS, Home
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class AuthSignupHomeFirstname(Home):
    def get_auth_signup_qcontext(self):
        SIGN_UP_REQUEST_PARAMS.update(["firstname", "lastname"])
        return super().get_auth_signup_qcontext()

    def _prepare_signup_values(self, qcontext):
        values = {key: qcontext.get(key) for key in ("login", "firstname", "lastname", "password")}
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get("password") != qcontext.get("confirm_password"):
            raise UserError(_("Passwords do not match; please retype them."))
        if values["firstname"] and values["lastname"]:
            values["name"] = f"{values['firstname']} {values['lastname']}"  # only for avoiding error, will be computed
        supported_lang_codes = [code for code, _ in request.env["res.lang"].get_installed()]
        lang = request.context.get("lang", "")
        if lang in supported_lang_codes:
            values["lang"] = lang
        return values


class WebsiteSaleFirstname(WebsiteSale):
    def _handle_extra_form_data(self, extra_form_data, address_values):
        super()._handle_extra_form_data(extra_form_data, address_values)

        order = request.website.sale_get_order()
        partner = order.partner_id.sudo()

        values = {}

        if "firstname" in extra_form_data:
            values["firstname"] = extra_form_data.get("firstname")
        if "lastname" in extra_form_data:
            values["lastname"] = extra_form_data.get("lastname")

        partner.write(values)
