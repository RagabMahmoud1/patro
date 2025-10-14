# -*- coding: utf-8 -*-
from odoo import models, api
import re
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def fix_product_names_with_wrong_codes(self):
        """
        Fix product names that start with a wrong code.
        This happens when the name contains a reference number different from default_code.
        
        Example:
        - default_code: "9030"
        - name: "8015 - حزام ستان LV (نسخة)" 
        
        Will be fixed to:
        - name: "9030 - حزام ستان LV (نسخة)"
        """
        
        # Find all products with default_code
        products = self.search([('default_code', '!=', False)])
        
        fixed_count = 0
        for product in products:
            if not product.default_code or not product.name:
                continue
                
            # Check if name starts with a number followed by space and dash
            # Pattern: "1234 - rest of name" or "1234- rest of name"
            match = re.match(r'^(\d+)\s*-\s*(.+)$', product.name)
            
            if match:
                number_in_name = match.group(1)
                rest_of_name = match.group(2)
                
                # If the number in name is different from default_code
                if number_in_name != product.default_code:
                    # Replace the wrong number with the correct default_code
                    new_name = f"{product.default_code} - {rest_of_name}"
                    
                    _logger.info(f"Fixing product {product.id}: '{product.name}' -> '{new_name}'")
                    product.write({'name': new_name})
                    fixed_count += 1
            else:
                # If name doesn't start with a number, but has default_code
                # Check if we should add the code to the beginning
                # Only if the name doesn't already contain the default_code at the start
                if not product.name.startswith(product.default_code):
                    # Check if the name already has the pattern "T1234 -" or similar
                    if not re.match(r'^[A-Z]?\d+\s*-', product.name):
                        # Only add default_code if it's not already there
                        _logger.info(f"Product {product.id} name doesn't start with code: '{product.name}'")
                        # Uncomment the next lines if you want to prepend the code
                        # new_name = f"{product.default_code} - {product.name}"
                        # product.write({'name': new_name})
                        # fixed_count += 1
        
        _logger.info(f"Fixed {fixed_count} product names")
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'Fixed {fixed_count} product names',
                'type': 'success',
                'sticky': False,
            }
        }

    @api.model
    def write(self, vals):
        """
        Override write to automatically fix name when default_code changes
        """
        result = super(ProductTemplate, self).write(vals)
        
        # If default_code is being updated
        if 'default_code' in vals and vals.get('default_code'):
            for product in self:
                if product.name and product.default_code:
                    # Check if name starts with a wrong number
                    match = re.match(r'^(\d+)\s*-\s*(.+)$', product.name)
                    if match:
                        number_in_name = match.group(1)
                        rest_of_name = match.group(2)
                        
                        # If the number in name is different from new default_code
                        if number_in_name != product.default_code:
                            new_name = f"{product.default_code} - {rest_of_name}"
                            super(ProductTemplate, product).write({'name': new_name})
                            _logger.info(f"Auto-fixed product {product.id} name after default_code change")
        
        return result

