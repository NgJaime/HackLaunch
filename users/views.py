from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext

@login_required
def profile(request):
    return render(request, 'profile.html')


def require_email(request):
    if request.method == 'POST':
        request.session['saved_email'] = request.POST.get('email')
        backend = request.session['partial_pipeline']['backend']
        return redirect('social:complete', backend=backend)
    return render_to_response('email.html', RequestContext(request))


def validation_sent(request):
    return render(request, 'validation_sent.html')


def email_complete(request):
    return render(request, 'email_complete.html')


