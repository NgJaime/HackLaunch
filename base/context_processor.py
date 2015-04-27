from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from base.forms import InitialPassword
from social.apps.django_app.views import complete as social_complete


def login_input(request):
    if request.method == 'POST':
        form = InitialPassword(request.POST or None)

        if form.is_valid():
            result = social_complete(request, 'email')
        else:
            request.session.flush()
            return {'login_form': form}

    return {'login_form': InitialPassword()}
