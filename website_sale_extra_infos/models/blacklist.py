from odoo import fields, models


class BlacklistDate(models.Model):
    _name = "blacklist.date"
    _description = "Blocked Dates for Booking"

    name = fields.Char(required=True)
    date = fields.Date(required=True)
    active = fields.Boolean(
        string="Active", default=True, help="If unchecked, this blacklisted date entry will be ignored"
    )
