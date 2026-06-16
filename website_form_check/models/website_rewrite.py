from odoo import api, models


class WebsiteRewrite(models.Model):
    _inherit = "website.rewrite"

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)

        res["website_id"] = self.env["website"].get_current_website()

        return res
