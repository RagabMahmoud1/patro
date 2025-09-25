odoo.define('healthy_salesperson.hr_pop', function (require) {
    "use strict";


    var rpc = require('web.rpc');
    var _t = require('web.core')._t;
    const Registries = require('point_of_sale.Registries');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const {Gui} = require('point_of_sale.Gui');
    const ajax = require('web.ajax');
        var models = require('point_of_sale.models');
            var _super = models.Order;
    models.Order = models.Order.extend({
        export_as_JSON: function () {
            var json = _super.prototype.export_as_JSON.apply(this, arguments);
            json.sales_person = this.sales_person;
            return json;
        },
        init_from_JSON: function (json) {
            _super.prototype.init_from_JSON.apply(this, arguments);
            this.sales_person = json.sales_person;
        },




    });



    models.load_models({
        model: 'res.users',
        loaded: function (self, salespersons) {
            self.salespersons = salespersons;
        }
    });


    const {
        useState,
        useRef
    } = owl.hooks;


    class POSSalesPersonPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);

            this.state = useState({
                sales_person: this.props.sales_person,
            })


        }


        getPayload() {
            var selected_vals = [];
            var sales_person = this.state.sales_person;
            selected_vals.push(sales_person);
            return selected_vals
        }

        mounted() {


        }


        click_confirm() {
            var self = this;
            var payload = this.getPayload();
            var order = this.env.pos.get_order();
            order.sales_person = payload[0];
            self.trigger('close-popup');


        }


    }

    POSSalesPersonPopup.template = 'POSSalesPersonPopup';
    POSSalesPersonPopup.defaultProps = {
        confirmText: 'Select',
        cancelText: 'Cancel',
        title: 'Set Sales Represtiative',
        body: '',
    };

    Registries.Component.add(POSSalesPersonPopup);
    return POSSalesPersonPopup;


});