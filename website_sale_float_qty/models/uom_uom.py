from odoo import fields, models


class Uom(models.Model):
    _inherit = "uom.uom"

    float_qty = fields.Boolean(
        "Float Qty",
        default=False,
        help="Defines if product with this Unit Of Measure \
            can be ordered with decimal quantities on the website.",
    )
