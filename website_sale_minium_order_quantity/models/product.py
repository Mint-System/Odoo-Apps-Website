import logging
_logger = logging.getLogger(__name__)
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    min_order_qty  = fields.Float(string='Minimum Order Qty', digits='Product Unit of Measure', default=1.0)
    
    @api.constrains('min_order_qty')
    def check_min_order_qty_valid(self):
        for product in self:
            if product.min_order_qty < 1:
                raise UserError(_('Minimum Order Quantity should be more than 0.'))

class ProductProduct(models.Model):
    _inherit = 'product.product'

    min_order_qty  = fields.Float(string='Minimum Order Qty', digits='Product Unit of Measure', default=1.0)
    
    @api.constrains('min_order_qty')
    def check_min_order_qty_valid(self):
        for product in self:
            if product.min_order_qty < 1:
                raise UserError(_('Minimum Order Quantity should be more than 0.'))
