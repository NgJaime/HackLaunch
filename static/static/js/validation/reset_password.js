resetPassword = function () {

        validate = function (password_id, confirmation_id) {
            var password = $('#' + password_id).val(),
                confirmation = $('#' + confirmation_id);

            var isValid = resetPasswordMessage.passwordStrength(password);

            if (isValid) {
                isValid = resetPasswordMessage.matchPasswords(password, confirmation);
            }

            return isValid;
        }

    return {
        validate: validate
    }
}


var resetPasswordValidation = new resetPassword();
