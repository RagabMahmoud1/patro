odoo.define('abdallah_pos_receipt_v15.pos_delivery_method',function(require) {
    "use strict";
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
        const Registries = require('point_of_sale.Registries');
    const { useState, useRef } = owl.hooks;
    const { Gui } = require('point_of_sale.Gui');
    const { core, hooks } = owl;
    const { onWillStart} = hooks;
    var delivery_type = {}
    class SetDeliveryMethodButton extends PosComponent {
        constructor() {
            super(...arguments);
            this.state = useState({
                name: this.get_current_delivery_method_name()
            })
            useListener('click', this.button_click);
        }
        async button_click() {
            var orders = this.env.pos.orders;
            var no_delivery_method = [{
            label: this.env._t("Sales Person Receipt"),
        }];
        const currentdelivery_method = this.env.pos.get_order().delivery_method
        const selection_list = [
                {
                    id: -1,
                    label: this.env._t('Sales Person Receipt'),
                    isSelected: false,
                },
            ];
            for (let del_meth of this.env.pos.delivery_sales_person_receipt) {
                selection_list.push({
                    id: del_meth.id,
                    label: del_meth.name,
                    isSelected: currentdelivery_method
                        ? del_meth.id === currentdelivery_method.id
                        : false,
                    item: del_meth,
                });
            }
             const { confirmed, payload: selected_delivery_method } = await this.showPopup(
                'SelectionPopup',
                {
                    title: this.env._t('Sales Person Receipt'),
                    list: selection_list,
                }
            );
                if (confirmed){
                    var order = this.env.pos.get_order();
                    order.delivery_method = selected_delivery_method;
                    const orderId = this.env.pos.get_order().uid;
                    var store_type= JSON.parse(localStorage.getItem(this.env.pos.db.name + 'order_type_reload')) || {};
                    store_type[this.env.pos.get_order().uid] = {'type': selected_delivery_method}
                    localStorage.setItem(this.env.pos.db.name + 'order_type_reload',JSON.stringify(store_type));
                    localStorage.getItem('order_type_reload')
                    if (selected_delivery_method!= undefined)
                      {
                    this.state.name = selected_delivery_method.name
                    }
                    else{
                    this.state.name='Sales Person Receipt'
                    }
                }
        }
        get_current_delivery_method_name(){
             var name = this.env._t('Sales Person Receipt');
            var item = localStorage.getItem(this.env.pos.db.name + 'order_type_reload')
            var obj=JSON.parse(item)
            var order_type = false
            if (obj){
                if (this.env.pos.get_order().uid in obj)
                order_type = obj[this.env.pos.get_order().uid]
            if (this.env.pos.get_order().orderlines.length ==0)
            {
                     name = this.env._t('Sales Person Receipt');
            }else if (order_type ){
                if ('type' in order_type){
                    name = order_type.type.name;
                    this.env.pos.get_order().delivery_method= order_type.type;
                }else{
                    name = 'Sales Person Receipt'
                }
            }
            return name;
            }
        }
}
SetDeliveryMethodButton.template = 'SetDeliveryMethodButton';
ProductScreen.addControlButton({
        component: SetDeliveryMethodButton,
        condition: function () {
            return true;
        },
        position: ['before', 'SetPricelistButton'],
    });
    Registries.Component.add(SetDeliveryMethodButton);
    return SetDeliveryMethodButton;
});
