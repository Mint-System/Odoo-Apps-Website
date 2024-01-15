from odoo import fields, models


class ProductTemplateWebsiteDescription(models.Model):
    _inherit = "product.template"

    web_description = fields.Text(
        "Website Description",
        help="This description will show up on website as product description.",
    )
