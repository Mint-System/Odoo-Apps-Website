from odoo import fields, models


class BlacklistCustomer(models.Model):
    _name = "blacklist.customer"
    _description = "Blacklist for Customers"

    name = fields.Char()
    email = fields.Char()
    street = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    country_id = fields.Many2one("res.country")

    reason = fields.Char()
    active = fields.Boolean(default=True)
    message = fields.Char()
