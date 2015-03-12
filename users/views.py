from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from users.models import CustomUser

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
    return render(request, 'validation_sent.html')


def email_complete(request):
    return render(request, 'email_complete.html')


