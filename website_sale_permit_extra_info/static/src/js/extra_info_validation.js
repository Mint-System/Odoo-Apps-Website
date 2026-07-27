/** @website-module */

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ExtraInfosForm = publicWidget.Widget.extend({
    selector:
        ".js_extra_info_form, form[data-model_name='sale.order'], form.o_extra_info_validation",
    events: {
        "click .s_website_form_send": "_onWebsiteFormSend",
        "focus input[name='date_from']": "_onDateInteract",
        "click input[name='date_from']": "_onDateInteract",
        "change input[name='date_from']": "_onDateInteract",
        "keyup input[name='date_from']": "_onDateInteract",
        "focus input[name='birthdate_date']": "_onDateInteract",
        "change input[name='birthdate_date']": "_onDateInteract",
        "keyup input[name='birthdate_date']": "_onDateInteract",
        "change input[name='photo']": "_onPhotoChange",
    },
    start() {
        console.log("ExtraInfosForm initialized");
        // Prevent widget from initializing in backend context where it's not needed
        if (!this.el.closest(".o_website_frontend")) {
            // Check if we're in a context where this widget should run
            // If not in website context, exit early to avoid errors in backend
            const isWebsiteContext =
                window.location.pathname.startsWith("/shop/") ||
                window.location.pathname.startsWith("/website/") ||
                this.el.closest(".s_website_form");

            if (!isWebsiteContext) {
                return Promise.resolve(); // Early return if not in proper context
            }
        }

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
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({}),
            });

            const data = await resp.json();
            if (data && data.result) {
                this.params = {...this.params, ...data.result}; // Merge with defaults
            }
            console.log("params :", this.params);
        } catch (e) {
            console.error("Could not fetch params", e);
            // Keep default params values if fetch fails
        }
    },

    _onPhotoChange(ev) {
        const input = ev.currentTarget;
        const file = input.files && input.files[0];

        let preview = this.el.querySelector("#photo_preview");

        if (!preview) {
            return;
        }

        if (!file || !file.type.startsWith("image/")) {
            preview.src = "";
            preview.style.display = "none";
            return;
        }

        const url = URL.createObjectURL(file);
        preview.src = url;
        preview.style.display = "block";
    },

    _onWebsiteFormSend(ev) {
        this._clearErrors();
        let hasError = false;
        const dateInput = this.el.querySelector("input[name='date_from']");
        const birthdateInput = this.el.querySelector("input[name='birthdate_date']");
        const fileInput = this.el.querySelector("input[name='photo']");
        const rawDateInput = dateInput?.value;
        const rawBirthdateInput = birthdateInput?.value;

        if (!rawDateInput && dateInput) {
            hasError = true;
            this._showError(dateInput, "Bitte ein gültiges Datum eingeben.");
        }

        if (!rawBirthdateInput && birthdateInput) {
            hasError = true;
            this._showError(
                birthdateInput,
                "Bitte ein gültiges Geburtsdatum eingeben."
            );
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

        // const year = parseInt(dateFrom.substring(0, 4));
        console.log("dateFrom: ", dateFrom);

        if (!dateFrom && dateInput) {
            hasError = true;
            this._showError(dateInput, "Ungültiges Datum.");
        } else if (dateFrom && dateInput) {
            // Date is valid, proceed with date-dependent validations
            const year = dateFrom.getFullYear();
            const currentYear = new Date().getFullYear();
            const years = this.params.patents_by_year || {};
            const yearStats = years[year] || {day: 0, week: 0, year: 0};

            const duration = this.params.duration || "day"; // default to "day"
            console.log("duration: ", duration);
            console.log("yearStats week:", yearStats.week);
            console.log("max week: ", this.params.max_week);

            if (this.params.future_only && dateFrom <= today && duration !== "year") {
                hasError = true;
                this._showError(dateInput, "Das Datum muss in der Zukunft liegen.");
            }

            if (this.params.future_only && year < currentYear && duration === "year") {
                hasError = true;
                this._showError(
                    dateInput,
                    "Sie können nicht für ein abgelaufenes Jahr ein Jahrespatent kaufen."
                );
            }

            if (
                duration != "year" &&
                Array.isArray(this.params.blacklisted_dates) &&
                this.params.blacklisted_dates.includes(normalizedDateInput)
            ) {
                hasError = true;
                this._showError(
                    dateInput,
                    "Dieses Datum ist nicht verfügbar. Bitte ein anderes wählen."
                );
            }

            // check sunday
            if (duration != "year" && dateFrom.getDay() === 0) {
                hasError = true;
                this._showError(
                    dateInput,
                    "Dieses Datum (Sonntag) ist nicht verfügbar. Bitte ein anderes wählen."
                );
            }

            // check if for year duration date is after March 31 of current year
            //if (duration === "year" && this._isAfterDeadlineOfCurrentYear(dateFrom)) {
            //    hasError = true;
            //    this._showError(
            //        dateInput,
            //        "Nach dem 31. März können Sie kein Jahrespatent mehr für das laufende Jahr bestellen."
            //    );
            //}

            // limit checks

            if (
                duration === "day" &&
                yearStats.year >= (this.params.max_year || Infinity)
            ) {
                hasError = true;
                this._showError(
                    dateInput,
                    `Es gibt bereits ein Jahrespatent ${year} für diese E-Mail-Adresse.`
                );
            }
            if (
                duration === "day" &&
                yearStats.day > (this.params.max_day || Infinity) &&
                yearStats.year === 0
            ) {
                hasError = true;
                this._showError(
                    dateInput,
                    `Im Jahr ${year} sind maximal ${this.params.max_day || "unbegrenzt"} Tagespatente erlaubt.`
                );
            }

            if (
                duration === "week" &&
                yearStats.week > (this.params.max_week || Infinity)
            ) {
                hasError = true;
                this._showError(
                    dateInput,
                    `Im Jahr ${year} ist nur ${this.params.max_week || 1} Wochenpatent erlaubt.`
                );
            }

            if (
                duration === "year" &&
                yearStats.year > (this.params.max_year || Infinity)
            ) {
                hasError = true;
                this._showError(
                    dateInput,
                    `Im Jahr ${year} ist nur ${this.params.max_year || 1} Jahrespatent erlaubt.`
                );
            }
        }

        if (!birthdate && birthdateInput) {
            hasError = true;
            this._showError(birthdateInput, "Ungültiges Geburtsdatum.");
        }

        // if (birthdate && birthdate >= today) {
        //     hasError = true;
        //     this._showError(birthdateInput, "Das Geburtsdatum muss in der Vergangenheit liegen.");

        // must be at least 14 years old
        const minAgeDate = new Date();
        minAgeDate.setFullYear(minAgeDate.getFullYear() - (this.params.min_age || 14));

        if (birthdate && birthdateInput && birthdate > minAgeDate) {
            hasError = true;
            this._showError(birthdateInput, "Sie müssen mindestens 14 Jahre alt sein.");
        }
        console.log("needs_photo", this.params.needs_photo);

        if (
            this.params.needs_photo &&
            !this.params.has_existing_photo &&
            fileInput &&
            fileInput.files.length === 0
        ) {
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

    _isAfterDeadlineOfCurrentYear(date) {
        const currentYear = new Date().getFullYear();
        const limitDate = new Date(currentYear, 2, 31);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        return date.getFullYear() === currentYear && today > limitDate;
    },

    _showError(input, message) {
        if (!input) {
            console.error("Input element is null or undefined");
            return;
        }

        // Highlight field
        input.classList.add("is-invalid");

        // Create error element
        const errorDiv = document.createElement("div");
        errorDiv.className = "invalid-feedback d-block o_extra_info_error";
        errorDiv.textContent = message;

        // Insert after input
        const parentContainer = input.closest(".s_website_form_field");
        if (parentContainer) {
            parentContainer.appendChild(errorDiv);
        } else {
            // If no container found, try adding next to input directly
            input.after(errorDiv);
        }
    },

    _clearErrors() {
        // Remove previous messages
        this.el.querySelectorAll(".o_extra_info_error").forEach((el) => el.remove());

        // Reset invalid state
        this.el.querySelectorAll(".is-invalid").forEach((el) => {
            el.classList.remove("is-invalid");
        });
    },

    _normalizeDate(raw) {
        // Input is often shown like "01.02.2025" or "01/02/2025"
        const parts = raw
            .replace(/[^0-9]/g, "-")
            .split("-")
            .filter(Boolean);
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
