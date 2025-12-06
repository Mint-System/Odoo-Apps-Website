/** @odoo-module **/

// This validator is for backend form validation
import { registry } from "@web/core/registry";
import { whenReady } from "@odoo/owl";

export class DateFromValidator = {
    /**
     * @param {Object} fields - name → value of form fields
     * @param {HTMLElement} form - the form DOM element
     */
    validate(fields, form) {
        const errors = {};

        const value = fields["date_from"];
        if (!value) {
            errors["date_from"] = "Please select a date.";
            return errors;
        }

        const selected = new Date(value);

        // Example blacklisted dates
        const blacklisted = [
            "2026-02-05",
            "2026-02-10",
            "2026-02-20",
        ].map((d) => new Date(d));

        if (blacklisted.some((d) => d.getTime() === selected.getTime())) {
            errors["date_from"] = "Selected date is not allowed.";
        }

        // Must be future
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        if (selected < today) {
            errors["date_from"] = "Date must be in the future.";
        }

        return errors;
    },
};

// Register this validator for website forms if needed
whenReady(() => {
    registry
        .category("website_form.validators")
        .add("date_from_validator", DateFromValidator);
});

