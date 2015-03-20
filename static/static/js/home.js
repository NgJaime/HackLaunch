$(document).ready(wrapResize);
$(window).resize(wrapResize);

function wrapResize() {
    var nav = $('.navbar');
    var full = $('#header-full-plan');
    var wrap = $('.wrap-primary-plan');
    var wrap2 = $('.wrap-pointers');

    //var sizeTop = nav.offset().top + nav.height();
    var sizeTop = 50;
    var sizeWrap = $(window).height() - sizeTop;
    wrap.css('min-height', sizeWrap + "px");
    wrap2.css('min-height', sizeWrap + "px");
}

validateSignup = function () {
    var email = document.forms["email_login"]["email"].value,
        password = document.forms["email_login"]["password"].value,
        result = true,
        message = "Please";

    if (!validatePassword(password)) {
        result = false;
        message += " choose a more complex password"
    }

    if (!validateEmail(email)) {
        result =  false;

        if (message !== "Please") {
            message += " & "
        }

        message += " provide a valid email address"
    }

    if (message !== "Please") {
        var password_strength_info = $("#password_strength_info");

        password_strength_info.find('.label').removeClass('hidden');
        password_strength_info.find('#password_strength_message').html(message);
        password_strength_info.removeClass('hidden');
    }

    return result;
}

validatePassword = function(password) {
    var result = zxcvbn(password);

    if (result.score < 3) {
        $("#signup_password_group").addClass("has-feedback has-error")
        return false;
    }

    $("#signup_password_group").removeClass("has-feedback has-error")
    return true;
}

validateEmail = function (email) {
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

    if (result === false) {
        $("#signup_email_group").addClass("has-feedback has-error")
    }
    else {
        $("#signup_email_group").removeClass("has-feedback has-error")
    }

    return result;
}
