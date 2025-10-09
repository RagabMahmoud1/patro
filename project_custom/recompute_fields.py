#!/usr/bin/env python3
"""
Script to recompute stored fields after module upgrade.
Run this from Odoo shell or copy the commands inside.
"""

# To run this, use:
# python3 odoo/odoo-bin shell -c conf/patro.conf -d YOUR_DATABASE_NAME

# Then paste these commands:

# Recompute color and size for all products
products = env['product.product'].search([])
print(f"Recomputing color and size for {len(products)} products...")
products._compute_color()
print("Done recomputing products!")

# Recompute fields for stock.quant
quants = env['stock.quant'].search([])
print(f"Updating {len(quants)} stock quants...")
for field in ['ore_id', 'session_id', 'categ_id', 'color', 'size', 'model_year']:
    print(f"  Recomputing {field}...")
    quants._compute_related_fields(field)
print("Done!")

# Recompute fields for stock.move.line
move_lines = env['stock.move.line'].search([])
print(f"Updating {len(move_lines)} stock move lines...")
for field in ['ore_id', 'session_id', 'categ_id', 'color', 'size', 'model_year']:
    print(f"  Recomputing {field}...")
    move_lines._compute_related_fields(field)
print("Done!")

env.cr.commit()
print("All fields recomputed and committed!")

