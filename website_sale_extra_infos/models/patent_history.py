import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatentHistory(models.Model):
    _name = "patent.history"
    _description = "History of Purchased Patents"

    partner_id = fields.Many2one("res.partner", required=True)
    product_id = fields.Many2one("product.product", required=True)
    duration = fields.Selection([("day", "Day"), ("week", "Week"), ("year", "Year")], required=True)
    year = fields.Integer(required=True)
    qty = fields.Float(default=1)

    sale_order_id = fields.Many2one("sale.order")
    sale_order_line_id = fields.Many2one("sale.order.line")
