# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResPartner(models.Model):
	_inherit = 'res.partner'

	date_of_birth = fields.Date(string='Date of Birth')
