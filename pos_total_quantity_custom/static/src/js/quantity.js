odoo.define('pos_total_quantity_custom.quantity_order', function (require) {
    "use strict";

    const OrderWidget = require('point_of_sale.OrderWidget');
    const Registries = require('point_of_sale.Registries');
    const {Gui} = require('point_of_sale.Gui');
    const QuantityWidgetCustom = OrderWidget =>
        class extends OrderWidget {

        _updateSummary() {
               super._updateSummary(...arguments);

              var order=this.env.pos.get_order();
              var qty=0;
              for (var i=0;i<order.get_orderlines().length;i++){
              qty+=order.get_orderlines()[i].quantity
              }
              this.state.quantity_count= qty;
        }
        };

    Registries.Component.extend(OrderWidget, QuantityWidgetCustom);

    return OrderWidget;






});
