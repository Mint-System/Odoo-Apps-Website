from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class CustomerPortalFirstname(CustomerPortal):

    def _get_mandatory_fields(self):
        mandatory_fields = super()._get_mandatory_fields()
        if request.httprequest.path == '/my/account':
            mandatory_fields += ["firstname", "lastname"]
        return mandatory_fields