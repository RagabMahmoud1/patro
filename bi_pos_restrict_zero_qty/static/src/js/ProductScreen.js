// BiProductScreen js
odoo.define('bi_pos_restrict_zero_qty.productScreen', function(require) {
    "use strict";

    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const rpc = require('web.rpc');

    const BiProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            constructor() {
                super(...arguments);
            }
            
            async _onClickPay() {
                var self = this;
                let order = this.env.pos.get_order();
                let lines = order.get_orderlines();
                let pos_config = self.env.pos.config;
                
                if (!pos_config.restrict_zero_qty) {
                    super._onClickPay();
                    return;
                }
                
                // Get product IDs from order lines (only storable products with POSITIVE quantity)
                // Negative quantities = returns, should NOT be restricted
                let productIds = [];
                let productQtyMap = {};  // product_id -> requested quantity (only positive/sales)
                
                for (let line of lines) {
                    let prd = line.product;
                    // Only check storable products with positive quantity (sales, not returns)
                    if (prd.type === 'product' && line.quantity > 0) {
                        if (!productQtyMap[prd.id]) {
                            productQtyMap[prd.id] = 0;
                            productIds.push(prd.id);
                        }
                        productQtyMap[prd.id] += line.quantity;
                    }
                }
                
                if (productIds.length === 0) {
                    // No storable products, allow payment
                    super._onClickPay();
                    return;
                }
                
                // Get location from picking_type
                let locationId = self.env.pos.pos_stock_location_id;
                
                if (!locationId && pos_config.picking_type_id) {
                    // Fetch location if not already loaded
                    try {
                        let pickingTypes = await rpc.query({
                            model: 'stock.picking.type',
                            method: 'read',
                            args: [[pos_config.picking_type_id[0]], ['default_location_src_id']],
                        });
                        if (pickingTypes.length > 0 && pickingTypes[0].default_location_src_id) {
                            locationId = pickingTypes[0].default_location_src_id[0];
                            self.env.pos.pos_stock_location_id = locationId;
                        }
                    } catch (err) {
                        console.warn('Error fetching location:', err);
                    }
                }
                
                console.log('=== BI_POS_RESTRICT: Checking stock at location:', locationId, '===');
                
                // Fetch quantities for these products at the location
                let quantities = {};
                try {
                    quantities = await rpc.query({
                        model: 'product.product',
                        method: 'get_qty_available_at_location',
                        args: [productIds, locationId],
                    });
                    console.log('=== BI_POS_RESTRICT: Quantities:', quantities);
                } catch (err) {
                    console.warn('Error fetching quantities, using global:', err);
                    // Fallback to global qty
                    for (let pid of productIds) {
                        let product = self.env.pos.db.get_product_by_id(pid);
                        quantities[pid] = product ? product.qty_available : 0;
                    }
                }
                
                // Check each product
                let hasError = false;
                for (let productId of productIds) {
                    let product = self.env.pos.db.get_product_by_id(productId);
                    let available = quantities[productId] || 0;
                    let requested = productQtyMap[productId];
                    
                    console.log('Product:', product.display_name, 'Available:', available, 'Requested:', requested);
                    
                    if (available <= 0 && requested > 0) {
                        hasError = true;
                        self.showPopup('ErrorPopup', {
                            title: self.env._t('Out of Stock'),
                            body: product.display_name + ' - ' + self.env._t('not available at this location') + ' (0)',
                        });
                    } else if (requested > available) {
                        hasError = true;
                        self.showPopup('ErrorPopup', {
                            title: self.env._t('Insufficient Stock'),
                            body: product.display_name + ' - ' + self.env._t('Available:') + ' ' + available + ', ' + self.env._t('Requested:') + ' ' + requested,
                        });
                    }
                }
                
                if (!hasError) {
                    super._onClickPay();
                }
            }
        };

    Registries.Component.extend(ProductScreen, BiProductScreen);

    return ProductScreen;

});
