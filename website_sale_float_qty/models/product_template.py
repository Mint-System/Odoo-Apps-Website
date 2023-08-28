from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_float_qty = fields.Boolean(
        store=True,
        related="uom_id.float_qty",
        help="If set, this product can be ordered with \
            decimal quantities on the website.",
    )

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1,
        pricelist=False,
        parent_combination=False,
        only_template=False,
    ):
        """Override
        Include the additional information of 'float_qty' based on the Unit of Measure
        set for the product. This allows to determine whether the product can be
        ordered with decimal quantities on the website.
        """
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            pricelist=pricelist,
            parent_combination=parent_combination,
            only_template=only_template,
        )

        if self.is_float_qty:
            combination_info["is_float_qty"] = True
        return combination_info
