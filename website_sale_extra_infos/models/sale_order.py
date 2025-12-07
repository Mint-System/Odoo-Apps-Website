import logging
from datetime import timedelta

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


from .config import REGION_SELECTION


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_from = fields.Date(
        compute="_compute_date_from"
        )

    date_to = fields.Date(
        compute="_compute_date_to")

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

    liability_insurance = fields.Boolean(
        compute="_compute_boolean_fields"
    )

    code_of_honour =  fields.Boolean(
        compute="_compute_boolean_fields"
    )

    strahlner_ordinance =  fields.Boolean(
        compute="_compute_boolean_fields"
    )

    minimum_age =  fields.Boolean(
        compute="_compute_boolean_fields"
    )

    photo_uploaded = fields.Boolean(
        default=False
    )



    # res.partner birthdate

    @api.depends("partner_id")
    def _compute_birthdate(self):
        for order in self:
            order.birthdate = self.partner_id.birthdate 

    @api.depends("order_line")
    def _compute_date_from(self):
        today = fields.Date.today()
        for order in self:
            if len(order.order_line) > 0:
               order.date_from = order.order_line[0].date_from if order.order_line[0].date_from else today
            else:
                order.date_from = today

    @api.depends("order_line")
    def _compute_date_to(self):
        for order in self:
            if len(order.order_line) > 0:
                order.date_to = order.order_line[0].date_to if order.order_line[0].date_to else order.date_from
            else:
                order.date_to = order.date_from

    @api.depends("order_line")
    def _compute_region(self):
        for order in self:
            if len(order.order_line) > 0:
                order.region = order.order_line[0].region if order.order_line[0].region else "none"
            else:
                order.region = "none"

    @api.depends("order_line")
    def _compute_boolean_fields(self):
        for order in self:
            order.liability_insurance = order.order_line[0].liability_insurance
            order.code_of_honour = order.order_line[0].code_of_honour
            order.strahlner_ordinance = order.order_line[0].strahlner_ordinance
            order.minimum_age = order.order_line[0].minimum_age



    