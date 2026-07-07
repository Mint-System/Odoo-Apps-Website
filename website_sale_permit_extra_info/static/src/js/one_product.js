/** @website-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import {rpc} from "@web/core/network/rpc";

publicWidget.registry.OneProductCart = publicWidget.Widget.extend({
    selector: ".oe_website_sale",

    start() {
        console.log("OneProductCart initialized");

        this.$el.on("click", "a.js_check_product.a-submit", async (ev) => {
            // Avoid infinite loop
            if (ev.originalEvent?.__oneProductSecondClick) {
                return;
            }

            ev.preventDefault();
            ev.stopPropagation();

            // 1. Clear cart
            await rpc("/shop/cart/clear", {});

            // 2. Re-trigger click so Odoo performs its normal flow
            const reClick = new MouseEvent("click", {bubbles: true, cancelable: true});
            reClick.__oneProductSecondClick = true;
            ev.currentTarget.dispatchEvent(reClick);
        });
    },
});
