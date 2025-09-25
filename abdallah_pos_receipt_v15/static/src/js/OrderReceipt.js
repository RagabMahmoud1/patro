odoo.define('ob_pos_custom_arabic_recpt.maiOrderReceipt', function(require) {
	"use strict";

	const OrderReceipt = require('point_of_sale.OrderReceipt');
	const Registries = require('point_of_sale.Registries');

	const maiOrderReceipt = OrderReceipt => 
		class extends OrderReceipt {
			constructor() {
				super(...arguments);
			}

			get order_seq(){
				function zero_pad(num,size){
					var s = ""+num;
					while (s.length < size) {
						s = "0" + s;
					}
					return s;
				}
				let order = this.env.pos.get_order();
               	return zero_pad(order.sequence_number,3);
			}

			get order_barcode() {
				let order = this.env.pos.get_order();
				let barcode = order.order_barcode.toString();
				if($('#order_barcode').length > 0){
					JsBarcode("#order_barcode", barcode);
				}
				return false;
			}
	};

	Registries.Component.extend(OrderReceipt, maiOrderReceipt);
	return OrderReceipt;
});