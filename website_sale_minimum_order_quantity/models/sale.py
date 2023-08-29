import logging
_logger = logging.getLogger(__name__)
from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _website_product_id_change(self, order_id, product_id, qty=0, **kwargs):
        product = self.env['product.product'].sudo().browse(product_id)
        if product.min_order_qty > 1.0: 
            if self._context.get('first_time_create') == False:
                qty = qty - product.min_order_qty + 1
            if self._context.get('first_time_create'):
                qty = product.min_order_qty
                self.env.context = dict(self.env.context)
                self.env.context.update({
                    'first_time_create':False
                })
        if qty < product.min_order_qty:
            qty = product.min_order_qty
        values = super(SaleOrder,self)._website_product_id_change(order_id=order_id, product_id=product_id, qty=qty)        
        return values
    
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        line = self.order_line.filtered(lambda o: o.product_id.id == product_id)
        if line.id:
            values = super(SaleOrder, self)._cart_update( product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)
        else:
            values = super(SaleOrder, self.with_context(first_time_create=True))._cart_update( product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)
        return values

class SaleInherit(models.Model):
    _inherit = 'sale.order.line'
  
    @api.constrains('product_uom_qty')
    def check_min_order_qty(self):
        messages=[]
        for line in self.filtered(lambda l: l.product_uom_qty and l.product_id.min_order_qty):
            rounding = line.product_uom.rounding            
            invalid_lines = line.filtered(lambda o: float_compare(o.product_uom_qty, o.product_id.min_order_qty, precision_rounding=rounding) < 0)
            if invalid_lines:
                for line in invalid_lines:
                    messages.append(_('Minimum Order Quantity for %s should be %s.') % (line.product_id.name, line.product_id.min_order_qty))
        if len(messages) > 0:
            message = '\n'.join(messages)
            raise ValidationError(message)
