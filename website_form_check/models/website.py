import logging
import re

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"

    check_ids = fields.One2many("website.form.check", inverse_name="website_id", string="Checks")

    def check_form_data(self, data_string):
        for check in self.check_ids:
            patterns = [p.strip() for p in check.patterns.split("\n") if p.strip()]

            for pattern in patterns:
                try:
                    if re.search(pattern, data_string):
                        redirect = check.redirect_id
                        if redirect:
                            return redirect.sudo().url_to
                        # fallback
                        return "/shop"
                except re.error:
                    continue

        return ""
