# -*- coding: utf-8 -*-

from odoo.fields import Boolean, Integer, Many2one
from odoo.models import TransientModel
from odoo import api


class ResConfigSettings(TransientModel):
    _inherit = 'res.config.settings'
    return_days = Integer(string="Return Days", required=False, default=14)

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        with_user = self.env['ir.config_parameter'].sudo()
        with_user.set_param('project_custom.return_days', self.return_days)

        return res

    @api.model
    def get_values(self):
        values = super(ResConfigSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        values['return_days'] = int(with_user.get_param('project_custom.return_days'))

        return values
