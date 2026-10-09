from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleDisableFields(WebsiteSale):
    def _get_mandatory_billing_address_fields(self, country_sudo):
        required_fields = super()._get_mandatory_billing_address_fields(country_sudo)
        return required_fields - request.website._get_address_optional_field_names()

    def _get_mandatory_delivery_address_fields(self, country_sudo):
        required_fields = super()._get_mandatory_delivery_address_fields(country_sudo)
        return required_fields - request.website._get_address_optional_field_names()
