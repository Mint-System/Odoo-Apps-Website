import json
import logging
from datetime import datetime

from odoo.http import request, route
from odoo.addons.website.controllers.form import WebsiteForm

_logger = logging.getLogger(__name__)

class WebsiteFormExtraInfo(WebsiteForm):

    @route('/website/form/shop.sale.order', type='http', auth="public", methods=['POST'], website=True)
    def website_form_saleorder(self, **kwargs):
        model_record = request.env.ref('sale.model_sale_order')
        try:
            data = self.extract_data(model_record, kwargs)
        except ValidationError as e:
            return json.dumps({'error_fields': e.args[0]})

        _logger.warning(f"data: {data}")

        order = request.website.sale_get_order()
        if not order:
            return json.dumps({'error': "No order found; please add a product to your cart."})

        custom = data.get('custom', '')

        custom_result = {}

        if ":" in custom:
            key, value = [x.strip() for x in custom.split(":", 1)]
            
            # Convert date
            try:
                date_obj = datetime.strptime(value, "%d.%m.%Y")
                value = date_obj.strftime("%Y-%m-%d")
            except Exception:
                pass

            custom_result[key] = value
            order.write(custom_result)

        if data['record']:
            order.write(data['record'])

        if data['attachments']:
            self.insert_attachment(model_record, order.id, data['attachments'])

        return json.dumps({'id': order.id})