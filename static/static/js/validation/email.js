
var emailFeedBack = function (formLocation, messageContainer) {
     function validateEmail(email, location) {
        function validateEmail(sEmail) {
            var filter = /^[\w\-\.\+]+\@[a-zA-Z0-9\.\-]+\.[a-zA-z0-9]{2,4}$/;
            if (filter.test(sEmail)) {
                return true;
            }
            else {
                return false;
            }
        }

        var result = false;

        if ($.trim(email).length == 0 || $("#fname").val() == "" || $("#lname").val() == "") {
            result = false
        }
        else if (validateEmail(email)) {
            result = true
        }

        return result;
    };

    var email = document.getElementById(formLocation)["email"].value,
        container = $("#" + messageContainer),

        errorElements = '<p id="error-message" style="margin: 10px 0px 0px"> \
                                <span id="login-warning" class="label label-danger"> Warning </span> \
                                <span id="message" style="margin-left:5px; color: #666"> \
                                    Please provide a valid email address \
                                </span> \
                        </p>';

    if (!validateEmail(email, formLocation)) {
        $("#" + formLocation).addClass("has-feedback has-error");
        container.append(errorElements);
        container.removeClass('hidden');
        return false;
    }

    return true;
};
