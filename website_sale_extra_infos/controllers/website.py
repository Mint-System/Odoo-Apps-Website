import base64
import json
import logging
from datetime import datetime

from odoo.http import request, route

from odoo.addons.website.controllers.form import WebsiteForm

_logger = logging.getLogger(__name__)


class WebsiteFormExtraInfo(WebsiteForm):
    @route("/website/form/shop.sale.order", type="http", auth="public", methods=["POST"], website=True)
    def website_form_saleorder(self, **kwargs):
        model_record = request.env.ref("sale.model_sale_order")
        # error = request.session.pop("form_error", None)
        try:
            data = self.extract_data(model_record, kwargs)
        except ValidationError as e:
            return json.dumps({"error_fields": e.args[0]})

        _logger.warning(f"data: {data}")

        order = request.website.sale_get_order()
        partner = order.partner_id
        if not order:
            return json.dumps({"error": "No order found; please add a product to your cart."})

        custom = data.get("custom", "")

        custom_result = self.parse_custom_field(custom)
        _logger.warning(f"custom_result: {custom_result}")
        custom_result = self.normalize_custom_fields(custom_result)

        birthdate = custom_result.pop("birthdate", None)

        order.order_line.write(custom_result)

        if order.partner_id and birthdate:
            order.partner_id.sudo().write({"birthdate": birthdate})

        if data["record"]:
            order.write(data["record"])

        if data["attachments"]:
            upload = data["attachments"][0]

            content = upload.read()
            b64 = base64.b64encode(content)
            filename = upload.filename
            mimetype = upload.mimetype

            if not partner.image_released:
                partner.sudo().write({"image_1920": b64})

            order.write({"photo_uploaded": True})
            # self.insert_attachment(model_record, order.id, data['attachments'])

        return json.dumps({"id": order.id})

    def parse_custom_field(self, text):
        result = {}
        for line in text.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)  # split only on the first colon
                key = key.strip()
                value = value.strip()
                result[key] = value
        return result

    def normalize_custom_fields(self, custom_fields_dict):
        custom_date = custom_fields_dict.get("date_from")
        birthdate = custom_fields_dict.get("birthdate")
        if custom_date:
            custom_fields_dict["date_from"] = datetime.strptime(custom_date, "%d.%m.%Y").date()
        if birthdate:
            custom_fields_dict["birthdate"] = datetime.strptime(birthdate, "%d.%m.%Y").date()
        return custom_fields_dict

    @route("/shop/cart/clear", type="json", auth="public", website=True)
    def clear_cart(self):
        order = request.website.sale_get_order()
        if order and order.order_line:
            order.order_line.unlink()
            request.website.sale_reset()
        return {"status": "ok"}
