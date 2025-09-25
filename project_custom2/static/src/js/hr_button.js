odoo.define('healthy_salesperson.sales_button', function (require) {
    "use strict";
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const {useListener} = require('web.custom_hooks');
    const {Gui} = require('point_of_sale.Gui');

    class POSSalesPersonButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.button_click);
        }
        button_click() {
            var order = this.env.pos.get_order();
            Gui.showPopup('POSSalesPersonPopup', {
                'sales_person': order.sales_person
            });

        }


    }


    POSSalesPersonButton.template = 'POSSalesPersonButton';
    ProductScreen.addControlButton({

        component: POSSalesPersonButton,
        'condition': function () {
            return true;
        },
    });

    Registries.Component.add(POSSalesPersonButton);

    return POSSalesPersonButton;


});