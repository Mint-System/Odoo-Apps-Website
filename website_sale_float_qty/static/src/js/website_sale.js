odoo.define('website_sale_float_qty.VariantMixin', function (require) {
'use strict';

// const {Markup} = require('web.utils');
var VariantMixin = require('sale.VariantMixin');
var publicWidget = require('web.public.widget');
var core = require('web.core');
var wSaleUtils = require('website_sale.utils');
require('website_sale.website_sale');

publicWidget.registry.WebsiteSale.include({
    /**
     * @override
     * @param {MouseEvent} ev
     * Add step value 0.1
     */
    onClickAddCartJSON: function (ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);

        // n

        var $meter_elem = $link.parents('div#product_details').find('span[id="float_qty"]');
        if (!$meter_elem.length)
        {
            // TODO find in another place?
            $meter_elem = $link.parents('div.css_quantity').find('span[id="float_qty"]');
        }
        if ($meter_elem.attr("value") !== "True"){
            return this._super.apply(this, arguments);
        } else {
            var step = 0.1;
            var $input = $link.closest('.input-group').find("input");
            const min = 0.1;
            var max = parseFloat($input.data("max") || Infinity);
            var previousQty = parseFloat($input.val() || 0, 10);

            // N
            var quantity = ($link.has(".fa-minus").length ? -step : step) + previousQty;

            var newQty = quantity > min ? (quantity < max ? quantity : max) : min;

            if (newQty !== previousQty) {
                $input.val(newQty.toFixed(1)).trigger('change');
            }
            return false;
    }

    },
    /**
     * Alter +, - Allow buying decimal quantity for float_qty.
     * Replace parseInt() to parseFloat() to get correct float value.
     * @override
     */
    _onChangeCartQuantity: function (ev) {
        var $input = $(ev.currentTarget);
        var $float_qty = $input.parents('div.css_quantity').find('span[id="float_qty"]');
        if ($float_qty.attr("value") !== "True") {
            return this._super.apply(this, arguments);
        } else {
            if ($input.data('update_change')) {
                return;
            }
            var value = parseFloat($input.val() || 0, 10);
            if (isNaN(value)) {
                value = 1;
            }
            var $dom = $input.closest('tr');
            var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
            var line_id = parseInt($input.data('line-id'), 10);
            var productIDs = [parseInt($input.data('product-id'), 10)];
            this._changeCartQuantity($input, value, $dom_optional, line_id, productIDs);
        }
    },
    /**
     * @private
     * @override
     *
     */
    _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
        var $float_qty = $input.parents('div.css_quantity').find('span[id="float_qty"]');
        if ($float_qty.attr("value") !== "True") {
            return this._super.apply(this, arguments);
        } else {
            _.each($dom_optional, function (elem) {
                $(elem).find('.js_quantity').text(value);
                productIDs.push($(elem).find('span[data-product-id]').data('product-id'));
            });
            $input.data('update_change', true);
            this._rpc({
                route: "/shop/cart/update_json",
                params: {
                    line_id: line_id,
                    product_id: parseInt($input.data('product-id'), 10),
                    set_qty: value,
                    is_float_qty: true,
                },
            }).then(function (data) {

                $input.data('update_change', false);
                var check_value = parseFloat($input.val() || 0, 10);
                if (isNaN(check_value)) {
                    check_value = 1;
                }
                if (value !== check_value) {
                    $input.trigger('change');
                    return;
                }
                debugger;
                sessionStorage.setItem('website_sale_cart_quantity', data.cart_quantity);
                if (!data.cart_quantity) {
                    return window.location = '/shop/cart';
                }
                $input.val(data.quantity);
                $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).text(data.quantity);

                wSaleUtils.updateCartNavBar(data);
                wSaleUtils.showWarning(data.warning);
                // Propagating the change to the express checkout forms
                core.bus.trigger('cart_amount_changed', data.amount, data.minor_amount);
            });
        }
    },
    /**
     * @private
     * @override
     *
     */
    _updateRootProduct($form, productId) {
        var $float_qty = $form.find('span[id="float_qty"]');
        if ($float_qty.attr("value") !== "True") {
            return this._super.apply(this, arguments);
        } else {
            const result = this._super.apply(this, arguments);
            debugger;
            const rootProduct = this.rootProduct;
            rootProduct.is_float_qty = true;
            this.rootProduct = rootProduct;
            return result;
        }
    },

});

return VariantMixin;

});
