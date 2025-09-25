odoo.define('ob_pos_custom_arabic_recpt.SubPaymentScreen', function(require) {

	const PaymentScreen = require('point_of_sale.PaymentScreen');
	const Registries = require('point_of_sale.Registries');

	const session = require('web.session');
	const PosComponent = require('point_of_sale.PosComponent');

	const { useListener } = require('web.custom_hooks');
	let core = require('web.core');
	let _t = core._t;

	const SubPaymentScreen = PaymentScreen => class extends PaymentScreen {
		constructor() {
			super(...arguments);
		}

		change_order_note() {
			let order= this.env.pos.get_order();
			let val = $("#order_note").val();
			order.set_order_note(val) ;
		}
	}

	Registries.Component.extend(PaymentScreen, SubPaymentScreen);

	return PaymentScreen;
});