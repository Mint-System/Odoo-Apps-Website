/** @website-module */

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ExtraInfosForm = publicWidget.Widget.extend({
    selector: "form.o_mark_required",   // target your form
    events: {
        "click .s_website_form_send": "_onWebsiteFormSend",
        "focus input[name='date_from']": "_onDateInteract",
        "click input[name='date_from']": "_onDateInteract",
        "change input[name='date_from']": "_onDateInteract",
        "keyup input[name='date_from']": "_onDateInteract",
        "focus input[name='birthdate']": "_onDateInteract",
        "change input[name='birthdate']": "_onDateInteract",
        "keyup input[name='birthdate']": "_onDateInteract",
    },
    start() {
        this.params = {
            blacklisted_dates: [],
            needs_photo: false,
            min_age: 14,
            future_only: true,
        };
        return this._fetchParams();
    },


    async _fetchParams() {
        try {
            const resp = await fetch("/website/get_params", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({})
            });

            const data = await resp.json();
            console.log("Blacklist:", data);
            this.params = data.result || this.params;
        } catch (e) {
            console.error("Could not fetch params", e);
        }
    },


    _onWebsiteFormSend(ev) {
        this._clearErrors();
        let hasError = false;
        const dateInput = this.el.querySelector("input[name='date_from']");
        const birthdateInput = this.el.querySelector("input[name='birthdate']");
        const fileInput = this.el.querySelector("input[type='file']");
        const rawDateInput = dateInput?.value;
        const rawBirthdateInput = birthdateInput?.value;


        if (!rawDateInput) {
            hasError = true;
            this._showError(dateInput, "Bitte ein gültiges Datum eingeben.");
        }

        if (!rawBirthdateInput) {
            hasError = true;
            this._showError(birthdateInput, "Bitte ein gültiges Geburtsdatum eingeben.");
        }

        if (hasError) {
            ev.preventDefault();
            ev.stopPropagation();
            ev.stopImmediatePropagation();
            return;
        }



        // Convert the user's date into YYYY-MM-DD for easier comparison
        const normalizedDateInput = this._normalizeDate(rawDateInput);
        const normalizedBirthdateInput = this._normalizeDate(rawBirthdateInput);

        const dateFrom = this._toDate(normalizedDateInput);
        const birthdate = this._toDate(normalizedBirthdateInput);

        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (!dateFrom) {
            hasError = true;
            this._showError(dateInput, "Ungültiges Datum.");
        }


        if (dateFrom && this.params.future_only && dateFrom <= today) {
            hasError = true;
            this._showError(dateInput, "Das Datum muss in der Zukunft liegen.");
        }

        if (this.params.blacklisted_dates.includes(normalizedDateInput)) {
            hasError = true;
            this._showError(dateInput, "Dieses Datum ist nicht verfügbar. Bitte ein anderes wählen.");
        }


        if (!birthdate) {
            hasError = true;
            this._showError(birthdateInput, "Ungültiges Geburtsdatum.");
        }


        // if (birthdate && birthdate >= today) {
        //     hasError = true;
        //     this._showError(birthdateInput, "Das Geburtsdatum muss in der Vergangenheit liegen.");

        // must be at least 14 years old
        const minAgeDate = new Date();
        minAgeDate.setFullYear(minAgeDate.getFullYear() - this.params.min_age);

        if (birthdate > minAgeDate) {
            hasError = true;
            this._showError(birthdateInput, "Sie müssen mindestens 14 Jahre alt sein.");
        }
        console.log("needs_photo", this.params.needs_photo)

        if (this.params.needs_photo && fileInput?.files.length === 0) {
            this._showError(fileInput, "Bitte eine Datei hochladen.");
            hasError = true;
        }

        if (hasError) {
            ev.preventDefault();
            ev.stopPropagation();
            ev.stopImmediatePropagation();
            return false;
        }
    },

    _onDateInteract() {
        this._clearErrors();
    },

    _showError(input, message) {
        // Highlight field
        input.classList.add("is-invalid");

        // Create error element
        const errorDiv = document.createElement("div");
        errorDiv.className = "invalid-feedback d-block o_extra_info_error";
        errorDiv.textContent = message;

        // Insert after input
        input.closest(".s_website_form_field").appendChild(errorDiv);
    },

    _clearErrors() {
        // Remove previous messages
        this.el.querySelectorAll(".o_extra_info_error").forEach(el => el.remove());

        // Reset invalid state
        this.el.querySelectorAll(".is-invalid").forEach(el => {
            el.classList.remove("is-invalid");
        });
    },

    _normalizeDate(raw) {
        // Input is often shown like "01.02.2025" or "01/02/2025"
        const parts = raw.replace(/[^0-9]/g, "-").split("-").filter(Boolean);
        // reorder into ISO format (yyyy-mm-dd)
        if (parts.length === 3) {
            // detect user locale (dd-mm-yyyy or mm-dd-yyyy)
            if (parts[0].length === 4) {
                // already yyyy-mm-dd
                return `${parts[0]}-${parts[1].padStart(2, "0")}-${parts[2].padStart(2, "0")}`;
            }
            // assume dd-mm-yyyy
            return `${parts[2]}-${parts[1].padStart(2, "0")}-${parts[0].padStart(2, "0")}`;
        }
        return raw;
    },
    _toDate(str) {
        if (!str) return null;
        const d = new Date(str);
        return isNaN(d) ? null : d;
    },

});

