odoo.define('bi_pos_restrict_zero_qty.pos', function(require) {
    "use strict";

    const models = require('point_of_sale.models');

    // Load product fields
    models.load_fields('product.product', ['qty_available', 'type']);

    // Store the stock location ID (will be fetched on first payment check)
    models.PosModel.prototype.pos_stock_location_id = null;
});
