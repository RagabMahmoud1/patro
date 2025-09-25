odoo.define('project_custom.price_list', function (require) {
    "use strict";

    const SetPricelistButton = require('point_of_sale.SetPricelistButton');
    const Registries = require('point_of_sale.Registries');
        var models = require('point_of_sale.models');

      models.load_models(
          {
        model:  'res.users',
        fields: ['name','company_id', 'id', 'groups_id', 'lang','can_edit_price_list'],
        domain: function(self){ return [['company_ids', 'in', self.config.company_id[0]],'|', ['groups_id','=', self.config.group_pos_manager_id[0]],['groups_id','=', self.config.group_pos_user_id[0]]]; },
        loaded: function(self,users){
            users.forEach(function(user) {
                user.role = 'cashier';
                user.groups_id.some(function(group_id) {
                    if (group_id === self.config.group_pos_manager_id[0]) {
                        user.role = 'manager';
                        return true;
                    }
                });
                if (user.id === self.session.uid) {
                    self.user = user;
                    self.employee.name = user.name;
                    self.employee.role = user.role;
                    self.employee.user_id = [user.id, user.name];
                    self.employee.can_edit_price_list = user.can_edit_price_list;
                }
            });
            self.users = users;
            self.employees = [self.employee];
            self.set_cashier(self.employee);
        },
    }

      );

    const CustomSetPricelistButton = SetPricelistButton =>
        class extends SetPricelistButton {
                async onClick() {
            // Create the list to be passed to the SelectionPopup.
            // Pricelist object is passed as item in the list because it
            // is the object that will be returned when the popup is confirmed.
            const selectionList = this.env.pos.pricelists.map(pricelist => ({
                id: pricelist.id,
                label: pricelist.name,
                isSelected: pricelist.id === this.currentOrder.pricelist.id,
                item: pricelist,
            }));

            const { confirmed, payload: selectedPricelist } = await this.showPopup(
                'SelectionPopup2',
                {
                    title: this.env._t('Select the pricelist'),
                    list: selectionList,
                }
            );

            if (confirmed) {
                this.currentOrder.set_pricelist(selectedPricelist);
            }
        }

        };

    Registries.Component.extend(SetPricelistButton, CustomSetPricelistButton);

    return SetPricelistButton;






});