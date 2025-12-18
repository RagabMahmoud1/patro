odoo.define('rgb_fix_pos_pl.models', function (require) {
    "use strict";

    const models = require('point_of_sale.models');
    const utils = require('web.utils');
    const field_utils = require('web.field_utils');
    const round_pr = utils.round_precision;

    const Orderline = models.Orderline.extend({
        // Force base list price to use the product's own lst_price instead of default pricelist
        get_lst_price: function () {
            if (this.get_product().lst_price) {
                return this.get_product().lst_price;
            } else {
                return this.product.get_price(this.pos.default_pricelist, 1, 0)
            }
        },

        
    });

    models.Orderline = Orderline;
    return models;
});
