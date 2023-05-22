from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'

    def sale_get_order(self, force_create=False, update_pricelist=False):
        """Do not update pricelist."""
        return super().sale_get_order(force_create=force_create, update_pricelist=False)