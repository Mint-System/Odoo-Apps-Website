# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_frontend_writable_fields(self):
        """Defines the fields a portal/public user can change on their contact and address records.
        Have to allow portal/website users to set the address type (person/company)."""
        frontend_writable_fields = super()._get_frontend_writable_fields()
        frontend_writable_fields.add("is_company")
        return frontend_writable_fields
