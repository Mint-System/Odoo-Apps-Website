/** @odoo-module **/

import publicWidget from "@web/portal/portal";

publicWidget.registry.WebsiteSaleExtraInfoDateValidation = publicWidget.Widget.extend({
    selector: '.js_website_sale_extra_info_form, .js_sale_order_extra_info, form[action*="/website/form/"]',
    
    start: function () {
        this._super.apply(this, arguments);
        
        // Initialize validation for date inputs
        this._initDateValidation();
    },

    _initDateValidation: function() {
        // Use a timeout to ensure DOM is fully loaded before attaching events
        setTimeout(() => {
            const dateInput = this.$el.find('input[name="date_from"]');
            if (dateInput.length === 0) {
                return; // No date input to validate
            }

            // Set min date attribute to prevent selecting past dates via HTML5 picker
            const today = new Date().toISOString().split('T')[0];
            dateInput.attr('min', today);

            // Attach validation on form submission
            this.$el.off('submit.dateValidation').on('submit.dateValidation', this._onFormSubmit.bind(this));
            
            // Attach real-time validation
            dateInput.off('blur.dateValidation').on('blur.dateValidation', this._validateDateInput.bind(this));
            dateInput.off('change.dateValidation').on('change.dateValidation', this._validateDateInput.bind(this));
        }, 100); // Small delay to ensure DOM is ready
    },

    _onFormSubmit: function(e) {
        const isValid = this._validateDateInput();
        if (!isValid) {
            e.preventDefault(); // Prevent form submission
            return false;
        }
    },

    _validateDateInput: function() {
        // Check if the element still exists in DOM
        if (this.$el.closest('body').length === 0) {
            return true; // Widget is detached, skip validation
        }
        
        const $dateInput = this.$el.find('input[name="date_from"]');
        
        // Check if date input still exists
        if ($dateInput.length === 0) {
            return true; // No date input to validate
        }
        
        const dateValue = $dateInput.val();
        
        // Clear previous errors
        this._clearError($dateInput);
        
        if (!dateValue) {
            this._showError($dateInput, 'Please select a start date.');
            return false;
        }

        // Check if date format is valid (YYYY-MM-DD)
        const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
        if (!dateRegex.test(dateValue)) {
            this._showError($dateInput, 'Please enter a valid date in YYYY-MM-DD format.');
            return false;
        }

        // Convert to date object and validate
        const selectedDate = new Date(dateValue);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        // Check if date is in the past
        if (selectedDate < today) {
            this._showError($dateInput, 'Date must be today or in the future.');
            return false;
        }

        // Additional validation - check if date is not too far in the future (optional)
        const maxFutureDate = new Date();
        maxFutureDate.setFullYear(maxFutureDate.getFullYear() + 2); // Allow up to 2 years in future
        if (selectedDate > maxFutureDate) {
            this._showError($dateInput, 'Date cannot be more than 2 years in the future.');
            return false;
        }

        // If validation passes
        this._clearError($dateInput);
        return true;
    },

    _showError: function($inputElement, message) {
        // Check if the element still exists before trying to modify it
        if ($inputElement.length === 0 || $inputElement.closest('body').length === 0) {
            return;
        }
        
        // Remove any existing error
        this._clearError($inputElement);
        
        // Add error styling
        $inputElement.addClass('o_website_form_error');
        
        // Create error message element
        const $errorElement = $('<div class="text-danger o_website_form_error_msg" style="font-size: 0.875em;">' + this._escapeHtml(message) + '</div>');
        
        // Insert error message after the input
        $inputElement.after($errorElement);
    },

    _clearError: function($inputElement) {
        if ($inputElement.length === 0 || $inputElement.closest('body').length === 0) {
            return; // Element doesn't exist anymore
        }
        
        $inputElement.removeClass('o_website_form_error');
        $inputElement.next('.o_website_form_error_msg').remove();
    },
    
    // Helper function to escape HTML to prevent XSS
    _escapeHtml: function(text) {
        var map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };

        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    },
    
    // Override destroy to clean up event handlers
    destroy: function() {
        const dateInput = this.$el.find('input[name="date_from"]');
        if (dateInput.length > 0) {
            dateInput.off('blur.dateValidation');
            dateInput.off('change.dateValidation');
        }
        this.$el.off('submit.dateValidation');
        this._super.apply(this, arguments);
    }
});