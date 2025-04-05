import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            helm_repo_ids = order.order_line.product_id.helm_repo_id
            for repo_id in helm_repo_ids:
                repo_id.install_chart()
        return res
