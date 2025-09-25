odoo.define('pos_discount.pos_total_quantity_custom', function (require) {
  "use strict";

  var models = require('point_of_sale.models');

var super_order_model = models.Order.prototype;
models.Order = models.Order.extend({
    export_for_printing: function () {
        const result = super_order_model.export_for_printing.apply(this, arguments);
        console.log("D><D<D<D",this)
         var qty=0;
         for (var i=0;i<this.get_orderlines().length;i++){
              qty+=this.get_orderlines()[i].quantity
              }
        result['quantity_count']=qty;
        result['total_items']=this.get_orderlines().length;




        return result;
    },
});



});
