# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    # _name = "product.template"
    # _inherit = ["product.template"]
    _inherit = "product.template"

    disable_add_to_cart = fields.Boolean(
        related='website_ribbon_id.disable_add_to_cart',
        string="Add to Cart Disabled",
        store=False  # or True if you need search/filter
    )

    def _can_be_added_to_cart(self):
        res = super()._can_be_added_to_cart()

        if self.website_ribbon_id and self.website_ribbon_id.disable_add_to_cart:
            return False
        return res