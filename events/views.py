from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from models import Event


def event(request, slug):
    return render(request, 'event.html')

@login_required(login_url='/login/')
def register(request, slug):
    event = get_object_or_404(Event, slug=slug)
    event.users.add(request.user)
    return render(request, 'event.html' )
