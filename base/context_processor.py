from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from base.forms import InitialPassword
from social.apps.django_app.views import complete as social_complete

# todo cerate a second context processor for all other logins to avoid duplicate code
def login_input(request):
    if request.method == 'POST':
        form = InitialPassword(request.POST or None)

        if form.is_valid():
            if 'email_validation_address' in request.session:
                request.session.pop('email_validation_address')

                if 'partial_pipeline' in request.session \
                    and 'backend' in request.session['partial_pipeline'] \
                    and request.session['partial_pipeline']['backend'] == u'email':
                    request.session.pop('partial_pipeline')

            result = social_complete(request, 'email')
        else:
            return {'login_form': form}

    return {'login_form': InitialPassword()}
