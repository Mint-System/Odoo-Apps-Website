# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class WebsiteFormCheck(models.Model):
    _name = "website.form.check"
    _description = "Website Form Check"

    name = fields.Char()
    patterns = fields.Char()
    form_id = fields.Many2one(
        comodel_name='ir.ui.view',
        domain="[('key', 'like', 'website_sale%')]"
    )
    redirect_id = fields.Many2one(
        comodel_name='website.rewrite'
    )
    website_id = fields.Many2one(
        comodel_name='website',
        copy=False,
        readonly=True,
    )

    active = fields.Boolean(default=True)