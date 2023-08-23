odoo.define('website_sale_float_qty.VariantMixin', function (require) {
'use strict';

require('website_sale.website_sale');
var publicWidget = require('web.public.widget');
var core = require('web.core');
var wSaleUtils = require('website_sale.utils');


publicWidget.registry.WebsiteSale.include({
    /**
     * @override
     * Add check if product can be ordered with decimal quantity.
     * If so, add/remove quantity by 0.1.
     * @param {MouseEvent} ev
     *
     */
    onClickAddCartJSON: function (ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $spanFloatQty = $link.parents('div#product_details').find('span[id="float_qty"]');
        if (!$spanFloatQty.length)
        {
            debugger;
            $spanFloatQty = $link.parents('div.css_quantity').find('span[id="float_qty"]');
        }
        if ($spanFloatQty.attr("value") !== "True"){
            // Apply standard process.
            return this._super.apply(this, arguments);
        } else {
            var step = 0.1;
            var $input = $link.closest('.input-group').find("input");
            const min = 0.1;
            var max = parseFloat($input.data("max") || Infinity);
            var previousQty = parseFloat($input.val() || 0, 10);
            var quantity = ($link.has(".fa-minus").length ? -step : step) + previousQty;
            var newQty = quantity > min ? (quantity < max ? quantity : max) : min;

            if (newQty !== previousQty) {
                $input.val(newQty.toFixed(1)).trigger('change');
            }
            return false;
    }

    },
    /**
     * @override
     * Replaced parseInt() to parseFloat() to get correct float value,
     * if product can be ordered with decimal quantity
     * @private
     * @param {Event} ev
     */
    _onChangeCartQuantity: function (ev) {
        var $input = $(ev.currentTarget);
        var $spanFloatQty = $input.parents('div.css_quantity').find('span[id="float_qty"]');
        if ($spanFloatQty.attr("value") !== "True") {
            // Apply standard process
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
     * @override
     * If product can be ordered with decimal quantity, include information in
     * request to backend: is_float_qty: true.
     * @private
     */
    _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
        var $spanFloatQty = $input.parents('div.css_quantity').find('span[id="float_qty"]');
        if ($spanFloatQty.attr("value") !== "True") {
            // Apply standard process
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
     * @override
     * Include information is_float_qty = true when Add To Cart button clicked
     * if product can be ordered with decimal quantity.
     * @private
     * @param {Object} $form
     * @param {Number} productId
     */
    _updateRootProduct($form, productId) {
        var $spanFloatQty = $form.find('span[id="float_qty"]');
        if ($spanFloatQty.attr("value") !== "True") {
            // Apply standard process
            return this._super.apply(this, arguments);
        } else {
            debugger;
            const result = this._super.apply(this, arguments);
            const rootProduct = this.rootProduct;
            rootProduct.is_float_qty = true;
            this.rootProduct = rootProduct;
            return result;
        }
    },

});

});
