from website_sale_permit_extra_info.controllers.website import WebsiteFormExtraInfo
from odoo.http import route, request
from odoo.exceptions import ValidationError


class WebsiteFormExtraInfoCheck(WebsiteFormExtraInfo):

    def _prepare_saleorder_form_data(self, model_record, kwargs):
        prepared_data = super()._prepare_saleorder_form_data(model_record, kwargs)

        redirect_url = request.website.check_form_data(prepared_data)

        if redirect_url:
            return request.redirect(redirect_url)

        return prepared_data