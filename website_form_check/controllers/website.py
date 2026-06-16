import json
import logging

from odoo.exceptions import ValidationError
from odoo.http import request, route

from odoo.addons.website_sale.controllers.website import WebsiteSaleForm

from ..helpers.utils import _unicode_to_ascii

_logger = logging.getLogger(__name__)


class WebsiteSaleFormCheck(WebsiteSaleForm):
    def _generate_string(self, data):
        data_string = ""
        for key, value in data.items():
            if isinstance(value, str):
                data_string += value.replace(" ", "").replace("\n", "")

        # handle names
        order = request.website.sale_get_order()
        partner = order.partner_id

        parts = []
        if partner.firstname:
            parts.append(partner.firstname)
        if partner.lastname:
            parts.append(partner.lastname)

        name_parts = []
        if len(parts) == 2:
            name_parts = [parts[0], parts[1], "---", parts[1], parts[0]]  # Build [first, last, last, first]
        elif len(parts) == 1:
            name_parts = [parts[0]]
        else:
            name_parts = [partner.name]

        name_string = "".join(name_parts).lower()

        # Clean whitespace and newlines
        name_string = name_string.replace(" ", "").replace("\n", "")

        # Append email if exists
        email_string = partner.email or ""

        data_string = name_string + "---" + email_string + "---" + data_string
        data_string_ascii = _unicode_to_ascii(data_string)

        return data_string_ascii

    def _check_data(self, data):
        data_string = self._generate_string(data)
        redirect_url = request.website.check_form_data(data_string)

        return redirect_url

    @route("/website/form/shop.sale.order", type="http", auth="public", methods=["POST"], website=True)
    def website_form_saleorder(self, **kwargs):
        model_record = request.env.ref("sale.model_sale_order")
        try:
            data = self.extract_data(model_record, kwargs)
        except ValidationError as e:
            return json.dumps({"error_fields": e.args[0]})

        if data:
            redirect_url = self._check_data(data)
            if redirect_url:
                request.session["form_check_redirect"] = redirect_url

        return super().website_form_saleorder(**kwargs)
