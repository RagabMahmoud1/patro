# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class UomReport(models.TransientModel):
    _name = "uom.report.wiz"

    prods = fields.Many2many(comodel_name="product.product", string="Products")
    location_ids = fields.Many2many(comodel_name="stock.location", string="Locations",
                                    domain="[('usage','=','internal')]" )

    def get_qty(self,loc,product_id):
        quant_groups = self.env['stock.quant'].read_group(
                [
                    ('location_id', 'child_of', [loc]),
                    ('product_id', '=', product_id),
                ],
                ['quantity', 'product_id'],
                ['product_id'])
        if quant_groups:
            return quant_groups[0]['quantity']
        else:
            return 0






    def dynamic_view(self):
        cloumns = []
        locs = []
        domain = [('type', '=', 'product')]
        if self.prods:
            domain.append(('id', 'in', self.prods.ids))

        products = self.env['product.product'].search(domain)
        for product in products:
            temp = {}
            temp['product_name'] = product.display_name
            temp['product_barcode'] = product.barcode
            for loc in self.env['stock.location'].search([('id', 'in', self.location_ids.ids)]) or self.env['stock.location'].search([]):
                if loc.name not in locs:
                    locs.append(loc.name)
                temp[loc.name] =  self.get_qty(loc.id,product.id)
            cloumns.append(temp)

        print('cloumns',cloumns)

        return {
            'name': "Unit Of Measure Report",
            'type': 'ir.actions.client',
            'tag': 'uom_report_view',
            'cloumns': cloumns,
            'locs': locs,
        }

    def print_pdf(self):
        data = {'prods': self.prods.ids, 'location_ids': self.location_ids.ids}
        return self.env.ref('loc_report.uom_report_action').report_action(self, data=data, config=False)


class UomReport(models.AbstractModel):
    _name = 'report.loc_report.loc_report'

    def get_qty(self,loc,product_id):
        quant_groups = self.env['stock.quant'].read_group(
                [
                    ('location_id', 'child_of', [loc]),
                    ('product_id', '=', product_id),
                ],
                ['quantity', 'product_id'],
                ['product_id'])
        if quant_groups:
            return quant_groups[0]['quantity']
        else:
            return 0

    @api.model
    def _get_report_values(self, docids, data=None):
        location_ids = data.get('location_ids')
        prods = data.get('prods')
        cloumns = []
        locs = []
        domain = [('type', '=', 'product')]
        if prods:
            domain.append(('id', 'in', prods))

        products = self.env['product.product'].search(domain)
        for product in products:
            temp = {}
            temp['product_name'] = product.display_name
            temp['product_barcode'] = product.barcode
            for loc in self.env['stock.location'].search([('id', 'in', location_ids)]) or self.env[
                'stock.location'].search([]):
                if loc.name not in locs:
                    locs.append(loc.name)
                temp[loc.name] = self.get_qty(loc.id, product.id)
            cloumns.append(temp)
        docargs = {
            'cloumns': cloumns,
            'locs': locs,
        }


        return docargs
