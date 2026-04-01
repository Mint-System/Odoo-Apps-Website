# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class WebsiteFormCheck(models.Model):
    _name = "website.form.check"
    _description = "Website Form Check"

    name = fields.Char()
    patterns = fields.Char()
    redirect_id = fields.Many2one(comodel_name="website.rewrite")
    website_id = fields.Many2one(
        comodel_name="website",
        copy=False,
        readonly=True,
        default=lambda self: self.env['website'].get_current_website()
    )

    active = fields.Boolean(default=True)

