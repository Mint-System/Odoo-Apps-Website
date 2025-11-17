import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_update_order_line(self, product_id, quantity, order_line, **kwargs):
        order_line = super()._cart_update_order_line(product_id, quantity, order_line, **kwargs)

        # Apply fixed price discount
        percent_price = order_line.order_id.pricelist_id._get_percent_price(order_line.product_id, quantity)
        order_line.update({"discount": percent_price})

        return order_line
