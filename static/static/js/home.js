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

LoginElements = function(location) {
    var addedElements = false,
        location = location,
        password_strength_bar = null,
        password_strength_info = null,
        password_strength_message = null,

        mainMessage = '<div class="col-sm-12 col-md-6 col-md-offset-3"> \
                            <div id="password_strength_background" class="progress" style="margin-bottom: 10px;"> \
                                <div id="main_password_strength_bar" \
                                     class="progress-bar progress-bar-warning password_strength_bar" \
                                     role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="5" \
                                     style="width: 0"> \
                                </div> \
                            </div> \
                            <p id="main_password_strength_info" class="text-muted password_strength_info"> \
                            <span id="login-warning" class="label label-danger"> \
                                 Warning \
                            </span> \
                                <span id="main_password_strength_message" \
                                      style="margin-left:5px; color: white"></span> \
                            </p> \
                        </div>',

        profileMessage = '<div class="col-sm-12 col-md-6 col-md-offset-3"> \
                            <div id="password_strength_background" class="progress" style="margin-bottom: 10px;"> \
                                <div id="profile_password_strength_bar" \
                                     class="progress-bar progress-bar-warning password_strength_bar" \
                                     role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="5" \
                                     style="width: 0"> \
                                </div> \
                            </div> \
                            <p id="profile_password_strength_info" class="text-muted password_strength_info"> \
                            <span id="login-warning" class="label label-danger"> \
                                 Warning \
                            </span> \
                                <span id="profile_password_strength_message" \
                                      style="margin-left:5px; color: #666"></span> \
                            </p> \
                        </div>',

        topMessage = '<div> \
                            <div id="password_strength_background" class="progress" style="margin-bottom: 5px;"> \
                                <div id="top_password_strength_bar" \
                                     class="progress-bar progress-bar-warning password_strength_bar" \
                                     role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="5" \
                                     style="width: 0"> \
                                </div> \
                            </div> \
                            <p id="top_password_strength_info" style="margin: 0px 0px 0px"> \
                                <span id="login-warning" class="label label-danger"> \
                                    Warning \
                                </span> \
                                <span id="top_password_strength_message" \
                                      style="margin-left:5px; color: #666"></span> \
                            </p> \
                        </div>',

        addElements = function() {
            if (addedElements === false) {
                $("#" + location + "-login-message").empty();

                var element = $("#" + location + "-login-message");

                if (location === "main") {
                    element.append(mainMessage);
                }
                else if (location === "top") {
                    element.append(topMessage);
                }
                else if (location === "profile") {
                    element.append(profileMessage);
                }

                this.password_strength_bar = $("#" + location + "_password_strength_bar");
                this.password_strength_info = $("#" + location + "_password_strength_info");
                this.password_strength_message = $("#" + location + "_password_strength_message")

                addedElements = true;
            }
        };

    return {
        addElements: addElements,
        password_strength_bar: password_strength_bar,
        password_strength_info: password_strength_info,
        password_strength_message: password_strength_message
    }
};

mainLoginElements = new LoginElements("main");
topLoginElements = new LoginElements("top");
profileLoginElements = new LoginElements("profile");


validateSignup = function (location) {
    var email = document.getElementById(location + "-login-form")["email"].value,
        password = document.getElementById(location + "-login-form")["password"].value,
        result = true,
        message = "Please";

    if (!validatePassword(password, location)) {
        result = false;
        message += " choose a more complex password"
    }

    if (!validateEmail(email, location)) {
        result =  false;

        if (message !== "Please") {
            message += " & "
        }

        message += " provide a valid email address"
    }

    if (message !== "Please") {
        if (location === 'main') {
            mainLoginElements.addElements();
            mainLoginElements.password_strength_message.html(message);
            mainLoginElements.password_strength_info.removeClass('hidden');
        }
        else if (location === 'top') {
            topLoginElements.addElements();
            topLoginElements.password_strength_message.html(message);
            topLoginElements.password_strength_info.removeClass('hidden');
        }
    }

    return result;
};


validateEditProfile = function (location) {
    var email = document.getElementById(location + "-login-form")["email"].value,
        password = document.getElementById(location + "-login-form")["password"].value,
        result = true,
        message = "Please";

    if (!validatePassword(password, location)) {
        result = false;
        message += " choose a more complex password"
    }

    if (!validateEmail(email, location)) {
        result =  false;

        if (message !== "Please") {
            message += " & "
        }

        message += " provide a valid email address"
    }

    if (message !== "Please") {
        if (location === 'main') {
            mainLoginElements.addElements();
            mainLoginElements.password_strength_message.html(message);
            mainLoginElements.password_strength_info.removeClass('hidden');
        }
        else if (location === 'top') {
            topLoginElements.addElements();
            topLoginElements.password_strength_message.html(message);
            topLoginElements.password_strength_info.removeClass('hidden');
        }
    }

    return result;
};

validatePassword = function(password, location) {
    var result = zxcvbn(password);

    if (result.score < 3) {
        $("#" + location + "_signup_password_group").addClass("has-feedback has-error")
        return false;
    }

    $("#" + location + "_signup_password_group").removeClass("has-feedback has-error")
    return true;
};

validateEmail = function (email, location) {
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
        $("#" + location + "_signup_email_group").addClass("has-feedback has-error")
    }
    else {
        $("#" + location + "_signup_email_group").removeClass("has-feedback has-error")
    }

    return result;
};
