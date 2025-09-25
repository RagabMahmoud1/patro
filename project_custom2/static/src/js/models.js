odoo.define('project_custom.pos', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;

    models.Order = models.Order.extend({
        export_for_printing: function() {
            var receipt = _super_order.export_for_printing.apply(this, arguments);
            console.log(receipt)


            var salesPersonId = parseInt(this.pos.get_order().sales_person);
            var salesPerson = this.pos.salespersons.find(function(sales_person) {
                return sales_person.id === parseInt(salesPersonId);
            });
            receipt.sales_person_name = salesPerson ? salesPerson.name : '';


            receipt.config_name = this.pos.config && this.pos.config.name ? this.pos.config.name : 'Default POS';

            return receipt;
        }
    });
});