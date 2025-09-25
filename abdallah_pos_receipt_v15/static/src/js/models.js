odoo.define('abdallah_pos_receipt_v15.models', function (require) {
"use strict";

var models = require('point_of_sale.models');
models.load_models({
    model: 'res.users',
    fields: ['name'],
    domain: function(self){ return [['id','in',self.config.delivery_sales_person_receipt]]; },
    loaded: function(self,delivery_sales_person_receipt){
        self.delivery_sales_person_receipt = delivery_sales_person_receipt;
    }
});
    var _super_order = models.Order;
    models.Order = models.Order.extend({
        initialize: function (attr, options) {
            _super_order.prototype.initialize.call(this, attr, options);
            this.delivery_method = this.delivery_method || false;
        },
        export_as_JSON: function(){
            var json = _super_order.prototype.export_as_JSON.apply(this,arguments);
            json.delivery_method = this.delivery_method || false;
            json.delivery_sales_person_receipt_id  = this.delivery_method ? this.delivery_method.id : false;
            return json;
        },
        init_from_JSON: function(json){
            _super_order.prototype.init_from_JSON.apply(this,arguments);
            this.delivery_method = json.delivery_method || false;
        },
    });
});