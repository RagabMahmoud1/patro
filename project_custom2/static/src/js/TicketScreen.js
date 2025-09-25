odoo.define('project_custom.TicketScreen', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const TicketScreen = require('point_of_sale.TicketScreen');
    const Registries = require('point_of_sale.Registries');
    const {useAutofocus} = require('web.custom_hooks');
    const {posbus} = require('point_of_sale.utils');
    const {parse} = require('web.field_utils');
    const {useState, useContext} = owl.hooks;

    const PosResTicketScreen = (TicketScreen) =>
        class extends TicketScreen {
            _getSearchFields() {
                const fields = {
                    RECEIPT_NUMBER: {
                        repr: (order) => order.name,
                        displayName: this.env._t('Receipt Number'),
                        modelField: 'pos_reference',
                    },
                    PRODUCT: {
                        repr: (order) => order.get_orderlines(),
                        displayName: this.env._t('Products'),
                        modelField: 'lines.full_product_name',
                    },
                    DATE: {
                        repr: (order) => moment(order.creation_date).format('YYYY-MM-DD hh:mm A'),
                        displayName: this.env._t('Date'),
                        modelField: 'date_order',
                    },
                    CUSTOMER: {
                        repr: (order) => order.get_client_name(),
                        displayName: this.env._t('Customer'),
                        modelField: 'partner_id.display_name',
                    },
                };

                if (this.showCardholderName()) {
                    fields.CARDHOLDER_NAME = {
                        repr: (order) => order.get_cardholder_name(),
                        displayName: this.env._t('Cardholder Name'),
                        modelField: 'payment_ids.cardholder_name',
                    };
                }

                return fields;
            }
            check_days(order) {
                var a = moment(order.validation_date);
                var b = moment(new Date())
                var diffDays = b.diff(a, 'days');
                if (this._state.ui.searchDetails.fieldName=='RECEIPT_NUMBER' ){
                    if(this._state.ui.searchDetails.searchTerm){
                        return true;
                    }else {
                        return diffDays<=3;
                    }

                }else {
                    return diffDays<=3;

                }

            }



        };

    Registries.Component.extend(TicketScreen, PosResTicketScreen);

    return {TicketScreen};
});
