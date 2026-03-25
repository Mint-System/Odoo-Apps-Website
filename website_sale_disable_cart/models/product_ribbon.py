# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ProductRibbon(models.Model):
    # _name = "website_sale.product.ribbon"
    # _inherit = ["website_sale.product.ribbon"]
    _inherit = "product.ribbon"

    disable_add_to_cart = fields.Boolean(default=False)