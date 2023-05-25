odoo.define('website_sale_minimum_order_quantity.website_sale_min_order', function (require) {
    'use strict';
    var core = require('web.core');
    var _t = core._t;
    var core = require('web.core');
    var ajax = require('web.ajax')
    var publicWidget = require('web.public.widget');
    require('website_sale.website_sale');
    const { OptionalProductsModal } = require('@sale_product_configurator/js/product_configurator_modal');

    $(document).on('change', '.quantity[data-min]', function (ev) {
        var $input = this;
        var val = $(ev.target).val();
        var min = parseFloat($($input).data("min") || 0);
        if (min > 1.0 && val < min) {
            $('.quantity').val(min);
            $($input).closest('.css_quantity').popover({
                content: _t("Minimum Order Quantity is ") + min + ".",
                title: _t("Warning"),
                placement: "left",
                trigger: 'focus',
                html: true,
            });
            $($input).closest('.css_quantity').popover('show')
            setTimeout(function () {
                $('.css_quantity').popover('dispose')
            }, 3000);
        }
    });

    publicWidget.registry.WebsiteSale.include({
        /**
         * @override
         * @private
         */

        onClickAddCartJSON: function (ev) {

            ev.preventDefault();
            $('.css_quantity').popover('dispose')
            var $link = $(ev.currentTarget);
            var $input = $link.closest('.input-group').find("input");
            var min = parseFloat($input.data("min") || 0);
            var max = parseFloat($input.data("max") || Infinity);
            var previousQty = parseFloat($input.val() || 0, 10);
            var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
            if (quantity < min && min > 1) {
                $input.closest('.css_quantity').popover({
                    content: _t(`Minimum Quantity is ${min}.`),
                    title: _t("Warning"),
                    placement: "left",
                    trigger: 'focus',
                    html: true,
                });
                $input.closest('.css_quantity').popover('show');

                setTimeout(function () {
                    $('.css_quantity').popover('dispose')
                }, 3000);
            }
            this._super(ev);

        },

        _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {

            $('.css_quantity').popover('dispose');
            var self = this;
            var _super = this._super;
            var kwargs = arguments;
            this._rpc({
                route: "/get/product/min_order_qty",
                params: {
                    cval: value,
                    product_id: parseInt($input.data('product-id'), 10),
                    show_error: true
                }
            }).then(function (data) {
                if (data.warning && line_id) {
                    $input.val(data.qty);
                    $input.closest('.css_quantity').popover({
                        content: _t(data.warning),
                        title: _t("Warning"),
                        placement: "top",
                        trigger: 'focus',
                        html: true,
                    });
                    $input.closest('.css_quantity').popover('show');
                    setTimeout(function () {
                        $('.css_quantity').popover('dispose')
                    }, 3000);
                }
                else {
                    _super.apply(self, kwargs);
                }
            });
        }
    });

    OptionalProductsModal.include({
        start: function () {
            var qty = this.$el.find('input[name="add_qty"]').val()
            var def = this._super.apply(this, arguments);
            this.$el.find('input[name="add_qty"]').first().val(qty);
            return def
        },

        _onChangeQuantity: function (ev) {
            var $product = $(ev.target.closest('tr.js_product'));
            var qty = parseFloat($(ev.currentTarget).val());
            var $input = $(ev.currentTarget)
            $('.css_quantity').popover('dispose')
            var self = this;
            var _super = this._super;
            var kwargs = arguments;
            ajax.jsonRpc("/get/product/min_order_qty", 'call',
                {
                    'cval': qty,
                    'product_id': parseInt($product.find('.product_id').val(), 10),
                }
            ).then(function (data) {
                if (data.warning) {
                    $input.val(data.qty);
                    $input.closest('.css_quantity').popover({
                        content: _t(data.warning),
                        title: _t("Warning"),
                        placement: "top",
                        trigger: 'focus',
                        html: true,

                    });
                    $input.closest('.css_quantity').popover('show');
                    setTimeout(function () {
                        $('.css_quantity').popover('dispose')
                    }, 3000);
                }
                else {
                    _super.apply(self, kwargs);
                }
            });

        },


    })

})
