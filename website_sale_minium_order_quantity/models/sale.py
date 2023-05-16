import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def _website_product_id_change(self, order_id, product_id, qty=0, **kwargs):
        product = self.env['product.product'].sudo().browse(product_id)
        if product.product_tmpl_id.min_order_qty>1.0: 
            if self._context.get('first_time_create') == False:
                qty = qty-product.product_tmpl_id.min_order_qty+1
            if self._context.get('first_time_create'):
                qty = product.min_order_qty
                self.env.context = dict(self.env.context)
                self.env.context.update({
                'first_time_create':False
                })
        if qty < product.min_order_qty:
            qty = product.min_order_qty
        values = super(SaleOrderInherit,self)._website_product_id_change( order_id=order_id, product_id=product_id, qty=qty)        
        return values
    
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        line = self.order_line.filtered(lambda o: o.product_id.id == product_id)
        if line.id:
            values = super(SaleOrderInherit,self)._cart_update( product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, kwargs=kwargs)
        else:
            values = super(SaleOrderInherit,self.with_context(first_time_create=True))._cart_update( product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, kwargs=kwargs)
        return values

class SaleInherit(models.Model):
    _inherit = 'sale.order.line'
  
    @api.constrains('product_uom_qty')
    def check_min_order_qty(self):
        il=[]
        for line in self:
            rounding = line.product_uom.rounding
            io =  line.filtered(lambda o :float_compare(o.product_uom_qty, o.product_template_id.min_order_qty, precision_rounding=rounding) < 0)
            if io:
                for p in io:
                    il.append(_('Minimum Order Quantity for %s should be %s'%(p.product_template_id.name,p.product_template_id.min_order_qty)))
        if len(il) > 0:
            msg = '\n'.join(il)
            raise ValidationError(msg)
