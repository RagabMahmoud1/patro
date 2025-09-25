odoo.define('project_custom.barcode', function (require) {
"use strict";

var models = require('point_of_sale.models');
// New orders are now associated with the current table, if any.
var _super_order_line = models.Orderline.prototype;
models.Orderline = models.Orderline.extend({

    export_for_printing: function() {
        var json = _super_order_line.export_for_printing.apply(this,arguments);
        json.barcode = this.get_product().barcode;
        return json;
    },

});


});
