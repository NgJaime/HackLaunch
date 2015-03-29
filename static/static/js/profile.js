Profile = function () {

    var isValid = true,

        removeErrorOnValue = function (value, elementPrefix) {
            if (value.length > 0) {
                var errorElement = $("#" + elementPrefix + "-errors"),
                    inputElement = $("#" + elementPrefix + "-input"),
                    iconElement = $("#" + elementPrefix + "-icon");

                errorElement.addClass('hidden');
                iconElement.addClass('hidden');
                inputElement.removeClass('has-error');
                inputElement.removeClass('has-feedback');
            }
        },

        requires = function(value, elementPrefix) {
            if (value.length === 0) {
                var icon = $('#' + elementPrefix + '-icon');
                icon.removeClass('hidden')

                var errors = $('#' + elementPrefix + '-errors');
                errors.removeClass('hidden');

                errors.append("<p class='text-muted'><span style='color: red'>This field is required.</span><p>")

                var input = $('#' + elementPrefix + '-input');
                input.addClass('has-error has-feedback')

                isValid = false;
            }
        },


        validate = function () {
            var first_name = $('#id_first_name').val(),
                last_name = $('#last_name').val(),
                location = $('#id_location').val(),
                password = $('#password_confirmation'),
                confirmation = $('#id_password_confirmation');
                isValid = true;

            this.requires(first_name, 'first-name');
            this.requires(last_name, 'last-name');
            this.requires(location, 'location');

            return isValid;
        }

    return {
        removeErrorOnValue: removeErrorOnValue,
        validate: validate
    }
}


var profileValidation = new Profile();
