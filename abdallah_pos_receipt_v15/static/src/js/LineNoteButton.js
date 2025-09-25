odoo.define("ob_pos_custom_arabic_recpt.LineNoteButton", function (require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const ProductScreen = require('point_of_sale.ProductScreen');
	const { useListener } = require('web.custom_hooks');
	const Registries = require('point_of_sale.Registries');

	class LineNoteButton extends PosComponent {
		constructor() {
			super(...arguments);
			useListener('click', this.onClick);
		}
		get selectedOrderline() {
			return this.env.pos.get_order().get_selected_orderline();
		}
		async onClick() {
			if (!this.selectedOrderline) return;

			const { confirmed, payload: inputNote } = await this.showPopup('TextAreaPopup', {
				startingValue: this.selectedOrderline.get_order_line_note(),
				title: this.env._t('Enter Product Note'),
			});

			if (confirmed) {
				this.selectedOrderline.set_order_line_note(inputNote);
			}
		}
	}
	LineNoteButton.template = 'LineNoteButton';
	ProductScreen.addControlButton({
		component: LineNoteButton,
		condition: function() {
			return this.env.pos.config.on_product_line;
		},
	});
	Registries.Component.add(LineNoteButton);
	return LineNoteButton;
});
