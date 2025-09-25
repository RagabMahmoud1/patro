odoo.define('project_custom.cash', function (require) {
    "use strict";

    const CashMovePopup = require('point_of_sale.CashMovePopup');
    const CashMoveButton = require('point_of_sale.CashMoveButton');
    const Registries = require('point_of_sale.Registries');
    const { _t } = require('web.core');
    const { parse } = require('web.field_utils');
    var models = require('point_of_sale.models');
    models.load_models({
        model: 'cash.items',
        fields: ['id', 'name'],
        loaded: function (self, items) {
            self.items = items;
        }
    });

    const CustomCashMovePopup = CashMovePopup =>
        class extends CashMovePopup {
        async confirm() {
            try {
                parse.float(this.state.inputAmount);
                let cash = await this.check_cash(parse.float(this.state.inputAmount));
                console.log("::D", cash)
                if (this.state.inputType == 'out') {
                    if (parse.float(this.state.inputAmount) > cash.amount) {
                        alert("Not Allow")
                        return;
                    }

                }

            } catch (error) {
                this.state.inputHasError = true;
                this.errorMessage = this.env._t('Invalid amount');
                return;
            }
            if (this.state.inputType == '') {
                this.state.inputHasError = true;
                this.errorMessage = this.env._t('Select either Cash In or Cash Out before confirming.');
                return;
            }
            return super.confirm();
        }
         async check_cash() {
            try {
                const closingData = await this.rpc({
                    model: 'pos.session',
                    method: 'get_closing_control_data',
                    args: [[this.env.pos.pos_session.id]]
                });
                let cash=closingData.default_cash_details;
                return cash;

            } catch (error) {

                return 0;
            }
        }
         getPayload() {
            return {
                amount: parse.float(this.state.inputAmount),
                reason: this.state.inputReason.trim(),
                type: this.state.inputType,
                item_id: this.state.item_id,
            };
        }
        };

    Registries.Component.extend(CashMovePopup, CustomCashMovePopup);

    return CashMovePopup;






});
