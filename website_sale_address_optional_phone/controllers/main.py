import logging

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSaleExtended(WebsiteSale):
    def _get_mandatory_billing_address_fields(self, country_sudo):
        required_fields = super()._get_mandatory_billing_address_fields(country_sudo)
        required_fields.remove("phone")
        return required_fields

    def _get_mandatory_delivery_address_fields(self, country_sudo):
        required_fields = super()._get_mandatory_delivery_address_fields(country_sudo)
        required_fields.remove("phone")
        return required_fields
