# -*- coding: utf-8 -*-

from odoo import models, fields, api
from collections import defaultdict


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_grouped_move_lines_by_template(self):
        """
        Group move lines by product template instead of product variant.
        Returns a list of dictionaries with template info and total quantity.
        """
        self.ensure_one()
        grouped = defaultdict(lambda: {
            'product_tmpl_id': None,
            'product_tmpl_name': '',
            'quantity': 0.0,
            'uom': None,
            'variants': []
        })
        
        for move in self.move_ids_without_package:
            if move.product_id and move.state != 'cancel':
                template = move.product_id.product_tmpl_id
                key = template.id
                
                if not grouped[key]['product_tmpl_id']:
                    grouped[key]['product_tmpl_id'] = template
                    grouped[key]['product_tmpl_name'] = template.name
                    grouped[key]['uom'] = move.product_uom
                
                grouped[key]['quantity'] += move.product_uom_qty
                grouped[key]['variants'].append({
                    'name': move.product_id.display_name,
                    'qty': move.product_uom_qty,
                })
        
        return list(grouped.values())

    def get_move_lines_with_template_name(self):
        """
        Return move lines but with product template name for display.
        Useful for simple reports that just want template name.
        """
        self.ensure_one()
        lines = []
        
        for move in self.move_ids_without_package:
            if move.product_id and move.state != 'cancel':
                lines.append({
                    'product_name': move.product_id.product_tmpl_id.name,
                    'quantity': move.product_uom_qty,
                    'uom': move.product_uom.name,
                    'variant_info': move.product_id.display_name if move.product_id.product_variant_count > 1 else '',
                })
        
        return lines

