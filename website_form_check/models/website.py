from odoo import fields, models
from odoo.exceptions import ValidationError

class Website(models.Model):
    _inherit = 'website'

    check_ids = fields.One2many(
        'website.form.check', 
        inverse_name='website_id',
        string="Checks")


    def check_form_data(self, data):
        record = data.get('record', {})
        birthdate = data.get('birthdate')

        name = record.get('name', '')
        email = record.get('email', '')

        combined = f"{email}{name}{birthdate}".lower()

        for check in self.check_ids:
            patterns = [p.strip() for p in check.patterns.split("\n") if p.strip()]

            for pattern in patterns:
                try:
                    if re.search(pattern, combined):
                        if check.redirect_id:
                            return check.redirect_id.url
                        # fallback 
                        return '/shop'
                except re.error:
                    continue

        return ""