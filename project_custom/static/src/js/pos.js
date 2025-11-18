odoo.define('project_custom.pos_custom2', function (require) {
    "use strict";

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const models = require('point_of_sale.models');
    const core = require('web.core');
    const utils = require('web.utils');
    const _t = core._t;
    const round_pr = utils.round_precision;
    const _ = require('_');
    const moment = require('moment');
    
    // Extend Product to fix get_price for min_quantity = 1
    // The issue is that rules need to be sorted by min_quantity desc and the condition should be <= not <
    const Product = models.Product;
    Product = Product.extend({
        get_price: function(pricelist, quantity, price_extra){
            var self = this;
            var date = moment();

            if (pricelist === undefined) {
                alert(_t(
                    'An error occurred when loading product prices. ' +
                    'Make sure all pricelists are available in the POS.'
                ));
            }

            var category_ids = [];
            var category = this.categ;
            while (category) {
                category_ids.push(category.id);
                category = category.parent;
            }

            var pricelist_items = _.filter(pricelist.items, function (item) {
                return (! item.product_tmpl_id || item.product_tmpl_id[0] === self.product_tmpl_id) &&
                       (! item.product_id || item.product_id[0] === self.id) &&
                       (! item.categ_id || _.contains(category_ids, item.categ_id[0])) &&
                       (! item.date_start || moment.utc(item.date_start).isSameOrBefore(date)) &&
                       (! item.date_end || moment.utc(item.date_end).isSameOrAfter(date));
            });

            // Sort by min_quantity desc to apply the highest applicable rule first
            // This ensures rules with min_quantity=1 are checked before rules with min_quantity=0
            pricelist_items = _.sortBy(pricelist_items, function(item) {
                var min_qty = item.min_quantity || 0;
                return -min_qty; // Negative for descending order
            });

            var price = self.lst_price;
            if (price_extra){
                price += price_extra;
            }
            
            // Debug: log rules for debugging
            if (quantity === 1) {
                console.log('DEBUG: Product', self.name, 'Quantity:', quantity);
                console.log('DEBUG: Filtered rules:', pricelist_items.map(function(r) {
                    return {min_quantity: r.min_quantity || 0, price_discount: r.price_discount, compute_price: r.compute_price};
                }));
            }
            
            var applied_rule = _.find(pricelist_items, function (rule) {
                // Check if rule is applicable: quantity must be >= min_quantity
                // If min_quantity is 0 or null, rule applies to all quantities
                // If min_quantity is 1 and quantity is 1, then 1 >= 1 is true, so rule applies
                var min_qty = rule.min_quantity || 0;
                if (quantity < min_qty) {
                    if (quantity === 1) {
                        console.log('DEBUG: Rule skipped - min_quantity:', min_qty, 'quantity:', quantity);
                    }
                    return false;
                }
                
                if (quantity === 1) {
                    console.log('DEBUG: Rule applies - min_quantity:', min_qty, 'price_discount:', rule.price_discount);
                }

                if (rule.base === 'pricelist') {
                    price = self.get_price(rule.base_pricelist, quantity);
                } else if (rule.base === 'standard_price') {
                    price = self.standard_price;
                }

                if (rule.compute_price === 'fixed') {
                    price = rule.fixed_price;
                    return true;
                } else if (rule.compute_price === 'percentage') {
                    price = price - (price * (rule.percent_price / 100));
                    return true;
                } else {
                    var price_limit = price;
                    price = price - (price * (rule.price_discount / 100));
                    if (rule.price_round) {
                        price = round_pr(price, rule.price_round);
                    }
                    if (rule.price_surcharge) {
                        price += rule.price_surcharge;
                    }
                    if (rule.price_min_margin) {
                        price = Math.max(price, price_limit + rule.price_min_margin);
                    }
                    if (rule.price_max_margin) {
                        price = Math.min(price, price_limit + rule.price_max_margin);
                    }
                    return true;
                }

                return false;
            });

            return price;
        },
    });
    
    // Extend Orderline to override get_taxed_lst_unit_price
    // Use the actual product base price (lst_price) not the pricelist price
    const Orderline = models.Orderline;
    Orderline = Orderline.extend({
        get_taxed_lst_unit_price: function(){
            // Use the actual product base price (lst_price) not the pricelist price
            const product = this.get_product();
            const lstPrice = this.compute_fixed_price(product.lst_price);
            const taxesIds = product.taxes_id;
            const productTaxes = this.get_taxes_after_fp(taxesIds);
            const unitPrices = this.compute_all(productTaxes, lstPrice, 1, this.pos.currency.rounding);
            if (this.pos.config.iface_tax_included === 'total') {
                return unitPrices.total_included;
            } else {
                return unitPrices.total_excluded;
            }
        },
    });
    const L10nCoPosPaymentScreen = PaymentScreen =>
        class extends PaymentScreen {
            async _isOrderValid(isForceValidate) {
                if (!this.currentOrder.get_client()) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                    title: this.env._t('Please select the Customer'),
                    body: this.env._t(
                        'You need to select the customer before you can invoice or ship an order.'
                    ),
                });
                if (confirmed) {
                    this.selectClient();
                }
                return false;
            }
                if (this.currentOrder.get_client()) {
                if (!this.currentOrder.get_client().phone) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                    title: this.env._t('Please add phone for this customer'),
                    body: this.env._t(
                        'You need to add phone for  this customer before you can invoice or ship an order.'
                    ),
                });
                if (confirmed) {
                    this.selectClient();
                }
                return false;
            }
            }
                return super._isOrderValid(...arguments);
            }
        };

    Registries.Component.extend(PaymentScreen, L10nCoPosPaymentScreen);

    return PaymentScreen;






});
