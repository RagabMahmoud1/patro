from odoo import api, fields, models
from odoo.exceptions import ValidationError


class User(models.Model):
    _inherit='res.users'
    can_edit_price_list = fields.Boolean(string="Can Edit PriceList")
