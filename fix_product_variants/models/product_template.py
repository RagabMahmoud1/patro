# -*- coding: utf-8 -*-
from odoo import models, api
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def reset_template_attribute_lines(self, product_ids=None):
        """
        Reset attribute lines on product templates to force Odoo to recompute variants.
        Works like manually removing & re-adding lines.
        If product_ids is given, only reset those products.
        """ 
        
        if product_ids:
            products = self.browse(product_ids)
        else:
            # Get ALL products with attribute lines, not just those with multiple variants
            products = self.search([('attribute_line_ids', '!=', False)])

        for product in products:
            if product.attribute_line_ids:
                # Save old attribute lines
                old_lines = []
                for line in product.attribute_line_ids:
                    old_lines.append({
                        'attribute_id': line.attribute_id.id,
                        'value_ids': line.value_ids.ids,
                    })

                # Remove all attribute lines
                product.attribute_line_ids = [(5, 0, 0)]

                # Re-create attribute lines
                new_lines = []
                for line in old_lines:
                    new_lines.append((0, 0, {
                        'attribute_id': line['attribute_id'],
                        'value_ids': [(6, 0, line['value_ids'])],
                    }))
                product.attribute_line_ids = new_lines

        return True

 
