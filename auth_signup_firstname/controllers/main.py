import logging

from odoo.addons.web.controllers.home import Home, SIGN_UP_REQUEST_PARAMS
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)

class AuthSignupHomeFirstname(Home): 

    def get_auth_signup_qcontext(self):
        SIGN_UP_REQUEST_PARAMS.update(['firstname', 'lastname'])
        return super().get_auth_signup_qcontext()


    def _prepare_signup_values(self, qcontext):
        values = { key: qcontext.get(key) for key in ('login', 'firstname', 'lastname', 'password') }
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        if values["firstname"] and values["lastname"]:
            values["name"] = f"{values['firstname']} {values['lastname']}"  # only for avoiding error, wull be computed
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '')
        if lang in supported_lang_codes:
            values['lang'] = lang
        return values