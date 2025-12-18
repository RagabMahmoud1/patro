{
    "name": "RGB POS Pricelist Fix",
    "version": "15.0.1.0.0",
    "summary": "Ensure POS lines always show base price differences even when pricelist rules apply",
    "category": "Point of Sale",
    "author": "Patro",
    "license": "LGPL-3",
    "depends": ["point_of_sale", "product", "web"],
    "data": [],
    "assets": {
        "point_of_sale.assets": [
            "rgb_fix_pos_pl/static/src/js/rgb_fix_pos_pl.js"
        ]
    },
    "installable": True,
    "application": False,
    "auto_install": False
}
