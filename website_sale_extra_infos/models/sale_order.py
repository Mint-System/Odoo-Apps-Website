import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_from = fields.Date(
        string='Start Date', required=True,
        help='Start Date of Patent'
        ) 