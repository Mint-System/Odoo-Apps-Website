# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def write(self, vals):
        if "pricelist_id" in vals:
            for order in self:
                if order.state == "draft" and order.website_id:
                    if order.pricelist_id.id != vals["pricelist_id"] and order.order_line:
                        order.order_line.unlink()
        return super().write(vals)