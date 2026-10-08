from odoo import api, fields, models

# Partner fields that can be made optional. `country_id` is excluded on purpose, as the
# address form logic (states, zip, ...) depends on it.
OPTIONAL_ADDRESS_FIELDS = ["name", "email", "phone", "street", "city", "zip", "state_id"]
DEFAULT_OPTIONAL_ADDRESS_FIELDS = ["name", "email", "phone"]


class Website(models.Model):
    _inherit = "website"

    @api.model
    def _default_address_optional_field_ids(self):
        return self.env["ir.model.fields"].search(
            [("model", "=", "res.partner"), ("name", "in", DEFAULT_OPTIONAL_ADDRESS_FIELDS)]
        )

    address_optional_field_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        relation="website_address_optional_field_rel",
        string="Optional Address Fields",
        domain=[("model", "=", "res.partner"), ("name", "in", OPTIONAL_ADDRESS_FIELDS)],
        default=_default_address_optional_field_ids,
        help="These fields are not required in the shop address form.",
    )

    def _get_address_optional_field_names(self):
        """Return the names of the address fields that are optional for this website."""
        self.ensure_one()
        return set(self.sudo().address_optional_field_ids.mapped("name"))
