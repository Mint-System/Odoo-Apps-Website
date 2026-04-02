# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class WebsiteFormCheck(models.Model):
    _name = "website.form.check"
    _description = "Website Form Check"

    name = fields.Char()
    patterns = fields.Char(default="max.*muster.*max\\.muster@beispiel\\.com.*20.02.1980", help="Gebe hier das Muster an, das kontrolliert werden soll. Trage 'Vorname', 'Nachname', 'E-Mailadresse' und 'Geburtsdatum' in genau dieser Reihenfolge ein, mit '.*' als Trennzeichen. NB Eine '.' im Muster muss als '\\.' geschrieben werden, z. B. in der E-Mailadresse ('kunde@beispiel\\.com'), aber nicht beim Trennzeichen ('Max.*Muster').")
    redirect_id = fields.Many2one(comodel_name="website.rewrite")
    website_id = fields.Many2one(
        comodel_name="website",
        copy=False,
        readonly=True,
        default=lambda self: self.env['website'].get_current_website()
    )

    active = fields.Boolean(default=True)

