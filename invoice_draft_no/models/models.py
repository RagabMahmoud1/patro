# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit='account.move'

    @api.model
    def create(self, values):
        res=super(AccountMove, self).create(values)
        if res.move_type=="out_invoice":
            print('D>D>D',res._set_next_sequence())
            res.name=res._set_next_sequence()
        return res


