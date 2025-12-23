import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


from .config import REGION_SELECTION


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_from = fields.Date(compute="_compute_date_from")

    date_to = fields.Date(compute="_compute_date_to")

    birthdate = fields.Date(
        compute="_compute_birthdate",
    )

    region = fields.Selection(
        string="Region",
        selection=REGION_SELECTION,
        compute="_compute_region",
        store=False,
        readonly=True,
    )

    liability_insurance = fields.Boolean(compute="_compute_boolean_fields")

    code_of_honour = fields.Boolean(compute="_compute_boolean_fields")

    strahlner_ordinance = fields.Boolean(compute="_compute_boolean_fields")

    minimum_age = fields.Boolean(compute="_compute_boolean_fields")

    photo_uploaded = fields.Boolean(default=False)

    has_patents = fields.Boolean(compute="_compute_has_patents", store=False)

    @api.depends("partner_id")
    def _compute_birthdate(self):
        for order in self:
            order.birthdate = order.partner_id.birthdate if order.partner_id else False

    @api.depends("order_line")
    def _compute_date_from(self):
        today = fields.Date.today()
        for order in self:
            if order.order_line:
                first_line = order.order_line[0]
                order.date_from = first_line.date_from if first_line.date_from else today
            else:
                order.date_from = today

    @api.depends("order_line")
    def _compute_date_to(self):
        for order in self:
            if order.order_line:
                first_line = order.order_line[0]
                order.date_to = first_line.date_to if first_line.date_to else order.date_from
            else:
                order.date_to = order.date_from

    @api.depends("order_line")
    def _compute_region(self):
        for order in self:
            if order.order_line:
                first_line = order.order_line[0]
                order.region = first_line.region if first_line.region else "none"
            else:
                order.region = "none"

    @api.depends("order_line")
    def _compute_boolean_fields(self):
        for order in self:
            if order.order_line:
                first_line = order.order_line[0]
                order.liability_insurance = first_line.liability_insurance
                order.code_of_honour = first_line.code_of_honour
                order.strahlner_ordinance = first_line.strahlner_ordinance
                order.minimum_age = first_line.minimum_age
            else:
                order.liability_insurance = False
                order.code_of_honour = False
                order.strahlner_ordinance = False
                order.minimum_age = False

    def _compute_has_patents(self):
        for order in self:
            move_lines_is_patent = order.order_line.mapped("is_patent")
            _logger.warning(f"move_lines_is_patent: {move_lines_is_patent}")
            if any(move_lines_is_patent):
                self.has_patents = True
            self.has_patents = False

    def action_confirm(self):
        res = super(SaleOrder, self.with_context(prevent_delivery_creation=True)).action_confirm()
        for order in self:
            for line in order.order_line:
                product = line.product_id
                duration = product.duration
                if duration:
                    self.env["patent.history"].create(
                        {
                            "partner_id": order.partner_id.id,
                            "product_id": product.id,
                            "duration": duration,
                            "year": order.date_from.year,
                            "qty": line.product_uom_qty,
                            "sale_order_id": order.id,
                            "sale_order_line_id": line.id,
                        }
                    )
        return res
