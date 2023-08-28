from odoo import _, models
from odoo.exceptions import UserError
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_update(
        self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs
    ):
        """
        Override
        If an order for a product with a unit of measure that allows
        ordering with a floating-point quantity is requested, do not parse
        the quantity into an integer; instead, save it as a floating-point quantity.
        """
        if not kwargs.get("is_float_qty"):
            return super(SaleOrder, self)._cart_update(
                product_id=product_id,
                line_id=line_id,
                add_qty=add_qty,
                set_qty=set_qty,
                **kwargs,
            )
        else:
            self.ensure_one()
            self = self.with_company(self.company_id)

            if self.state != "draft":
                request.session.pop("sale_order_id", None)
                request.session.pop("website_sale_cart_quantity", None)
                raise UserError(
                    _(
                        "It is forbidden to modify a sales \
                            order which is not in draft status."
                    )
                )

            product = self.env["product.product"].browse(product_id).exists()
            if add_qty and (not product or not product._is_add_to_cart_allowed()):
                raise UserError(
                    _(
                        "The given product does not exist \
                            therefore it cannot be added to cart."
                    )
                )

            if product.lst_price == 0 and product.website_id.prevent_zero_price_sale:
                raise UserError(
                    _(
                        "The given product does not have \
                        a price therefore it cannot be added to cart."
                    )
                )

            if line_id is not False:
                order_line = self._cart_find_product_line(
                    product_id, line_id, **kwargs
                )[:1]
            else:
                order_line = self.env["sale.order.line"]

            quantity = 0
            if set_qty:
                quantity = set_qty
            elif add_qty is not None:
                if order_line:
                    quantity = order_line.product_uom_qty + (add_qty or 0)
                else:
                    quantity = add_qty or 0

            if quantity > 0:
                quantity, warning = self._verify_updated_quantity(
                    order_line,
                    product_id,
                    quantity,
                    **kwargs,
                )
            else:
                # If the line will be removed anyway, there is no need to verify
                # the requested quantity update.
                warning = ""

            order_line = self._cart_update_order_line(
                product_id, quantity, order_line, **kwargs
            )
            # Keep cart qty 1, when ordering decimal less than 1.
            if not self.cart_quantity and (
                (set_qty and set_qty > 0 and set_qty < 1)
                or (quantity and quantity > 0 and quantity < 1)
            ):
                self.cart_quantity = 1
            return {
                "line_id": order_line.id,
                "quantity": quantity,
                "option_ids": list(
                    set(
                        order_line.option_line_ids.filtered(
                            lambda l: l.order_id == order_line.order_id
                        ).ids
                    )
                ),
                "warning": warning,
            }
