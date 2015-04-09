from base.forms import InitialPassword


def login_input(request):

    return {
        'login_form': InitialPassword()
    }
