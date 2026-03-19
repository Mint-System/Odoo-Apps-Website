/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.MinQtyControl = publicWidget.Widget.extend({
    selector: "#product_detail .css_quantity",

    start() {
        this._apply();
    },

    events: {
        "click .js_add_cart_json": "_onClick",
        "change input.quantity": "_apply",
    },

    _getElements() {
        const input = this.el.querySelector("input.quantity");
        const minusBtn = this.el.querySelector(".fa-minus")?.closest("a");

        if (!input) return null;

        return {
            input,
            minusBtn,
            minQty: parseFloat(input.dataset.minQty) || 1,
        };
    },

    _apply() {
        const els = this._getElements();
        if (!els) return;

        let value = parseFloat(els.input.value) || els.minQty;

        if (value < els.minQty) {
            value = els.minQty;
            els.input.value = value;
        }

        if (els.minusBtn) {
            els.minusBtn.classList.toggle("disabled", value <= els.minQty);
        }
    },

    _onClick() {
        // wait for Odoo to update quantity, then re-check
        setTimeout(() => this._apply(), 0);
    },
});
