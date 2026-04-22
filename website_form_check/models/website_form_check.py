# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class WebsiteFormCheck(models.Model):
    _name = "website.form.check"
    _description = "Website Form Check"

    DEFAULT_PATTERN = r"max.*muster.*max\.muster@beispiel\.com.*20\.02\.1980"

    name = fields.Char()
    patterns = fields.Char(
        default=DEFAULT_PATTERN,
        help=(
            "Gib hier das Muster an, das kontrolliert werden soll.\n"
            "Reihenfolge: Vorname → Nachname → E-Mail → Geburtsdatum.\n"
            "Trennzeichen: '.*'.\n"
            "Punkte in der E-Mail und im Datum müssen als '\\.' geschrieben werden (z.B. 'kunde@beispiel\\.com')."
        ),
    )

    redirect_id = fields.Many2one(comodel_name="website.rewrite")
    website_id = fields.Many2one(
        comodel_name="website",
        copy=False,
        readonly=True,
        default=lambda self: self.env['website'].get_current_website()
    )

    is_active = fields.Boolean(default=True)

