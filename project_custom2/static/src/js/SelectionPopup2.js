odoo.define('point_of_sale.project_custom', function (require) {
    'use strict';

    const {useState} = owl.hooks;
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    // formerly SelectionPopupWidget
    class SelectionPopup2 extends AbstractAwaitablePopup {
        /**
         * Value of the `item` key of the selected element in the Selection
         * Array is the payload of this popup.
         *
         * @param {Object} props
         * @param {String} [props.confirmText='Confirm']
         * @param {String} [props.cancelText='Cancel']
         * @param {String} [props.title='Select']
         * @param {String} [props.body='']
         * @param {Array<Selection>} [props.list=[]]
         *      Selection {
         *          id: integer,
         *          label: string,
         *          isSelected: boolean,
         *          item: any,
         *      }
         */
        constructor() {
            super(...arguments);
            this.state = useState({selectedId: this.props.list.find((item) => item.isSelected)});
        }

        selectItem(itemId) {
            this.state.selectedId = itemId;
            this.confirm();
        }

        /**
         * We send as payload of the response the selected item.
         *
         * @override
         */
        getPayload() {
            const selected = this.props.list.find((item) => this.state.selectedId === item.id);
            return selected && selected.item;
        }

        async updatePriceList(event) {
            var list1 = [];
            if (event.target.value) {

                for (const item of this.props.list) {
                    if (item.label.includes(event.target.value)) {
                        list1.push(item)
                    }
                }
                this.props.list = list1
                this.render();
            } else {
                const selectionList = this.env.pos.pricelists.map(pricelist => ({
                    id: pricelist.id,
                    label: pricelist.name,
                    item: pricelist,
                }));
                this.props.list = selectionList
                this.render();
            }

        }
    }


    SelectionPopup2.template = 'SelectionPopup2';
    SelectionPopup2.defaultProps = {
        confirmText: 'Confirm',
        cancelText: 'Cancel',
        title: 'Select',
        body: '',
        list: [],
    };

    Registries.Component.add(SelectionPopup2);

    return SelectionPopup2;
});
