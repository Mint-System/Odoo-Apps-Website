import logging
_logger = logging.getLogger(__name__)
from odoo import http , fields, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.sale_product_configurator.controllers.main import ProductConfiguratorController


class WebsiteSale(WebsiteSale):
    @http.route()
    def product(self, product, category='', search='', **kwargs):
        res  = super(WebsiteSale, self).product(product,category,search,**kwargs)
        order = request.website.sale_get_order()
        line = False
        if order:
            line = order.order_line.filtered(lambda o: o.product_id.id == product.id)
        if not line:
            res.qcontext.update(min_qty=int(product.min_order_qty))
        return res

    @http.route('/get/product/min_order_qty',type="json", auth="public", website=True)
    def get_product_min_order_quantity(self, cval, product_id, show_error=False):
        product = request.env['product.product'].sudo().browse(int(product_id))
        
        min_qty = product.min_order_qty
        min_qty = product.product_tmpl_id.min_order_qty if min_qty <= 1.0 else 1.0

        if not product.product_template_attribute_value_ids:
            min_qty = product.product_tmpl_id.min_order_qty
        order = request.website.sale_get_order().exists()
        line = False
        if order:
            line = order.order_line.filtered(lambda o: o.product_id.id == product.id) 

        value = {} 
        cval = int(cval)
        if not line or show_error:
            if cval < min_qty and cval != 0:
                value.update({
                    'warning': _('Minimum Quantity is %s.') % (min_qty),
                    'qty': min_qty
                })
            return value
        value.update(qty=cval)
        return value

    @http.route()
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        product = request.env['product.product'].sudo().browse(int(product_id))
        order = request.website.sale_get_order()
        if order.id:
            line = order.order_line.filtered(lambda o: o.product_id.id == product.id) 
            if not line.id:
                if int(add_qty) < product.min_order_qty and 'product' in request.httprequest.referrer.split('/'):
                    return request.redirect(request.httprequest.referrer.split('?')[0]+'/?min_order_error=1&min_qty=%d'%product.min_order_qty)
                elif int(add_qty) < product.min_order_qty:
                    add_qty = product.min_order_qty
        return super(WebsiteSale,self).cart_update(product_id, add_qty, set_qty, **kw)

    # @http.route()
    # def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
    #     if add_qty:
    #         order = request.website.sale_get_order()
    #         if order.id:
    #             product = request.env['product.product'].sudo().browse(int(product_id))
    #             line = order.order_line.filtered(lambda o: o.product_id.id == product.id) 
    #             if not line.id:
    #                 if int(add_qty) < product.min_order_qty:
    #                     add_qty = product.min_order_qty
    #     return super(WebsiteSale,self).cart_update_json(product_id, line_id, add_qty, set_qty, display)

class ProductConfiguratorController(ProductConfiguratorController):
    
    def _show_optional_products(self, product_id, variant_values, pricelist, handle_stock, **kw):
        if hasattr(request,'website'):
            order = request.website.sale_get_order()
            product = request.env['product.product'].browse(int(product_id))
            line = False
            if order:
                line = order.order_line.filtered(lambda o: o.product_id.id == product.id) 
            add_qty = kw.get('add_qty')
            if not line:
                if add_qty and add_qty < product.min_order_qty or not add_qty:
                    kw.update(add_qty=int(product.min_order_qty))
        res = super(ProductConfiguratorController,self)._show_optional_products(product_id, variant_values, pricelist, handle_stock, **kw)
        return res
