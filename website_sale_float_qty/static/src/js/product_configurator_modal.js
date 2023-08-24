odoo.define('website_sale_float_qty.OptionalProductsModal', function (require) {
    "use strict";

const { OptionalProductsModal } = require('@sale_product_configurator/js/product_configurator_modal');

OptionalProductsModal.include({
    /**
     * @override
     * Add check if product can be ordered with decimal quantity in Optional Products Modal
     * wizard view.
     * If so, add/remove quantity by 0.1.
     * @param {MouseEvent} ev
     */
    onClickAddCartJSON: function (ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $spanFloatQty = $link.parents('div.css_quantity').find('span[id="float_qty"]');
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
});

});
