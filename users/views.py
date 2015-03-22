from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from users.models import CustomUser
from base.forms import InitialPassword
from social.apps.django_app.views import complete as social_complete
from django import forms
from django.core.validators import EmailValidator


@login_required
def profile_edit(request):
    return render(request, 'profile_edit.html')


def profile_view(request, slug):
    user = CustomUser.objects.get(slug=slug);

    return render(request, 'profile_view.html', {"profile": user})


def require_email(request):
    if request.method == 'POST':
        request.session['saved_email'] = request.POST.get('email')
        backend = request.session['partial_pipeline']['backend']
        return redirect('social:complete', backend=backend)
    return render_to_response('email.html', RequestContext(request))


def validation_sent(request):
    return render(request, 'validation_sent.html', {'email': request.session['email_validation_address']})


def email_complete(request):
    return render(request, 'email_complete.html')


def complete(request, backend, *args, **kwargs):

    if backend == u'email':
        form = InitialPassword(request.POST)

        if not form.is_valid():
            return render(request, 'home.html', {'form': form})

    return social_complete(request, backend, *args, **kwargs)


