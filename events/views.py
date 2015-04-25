from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from models import Event


def event(request, slug):
    this_event = get_object_or_404(Event, slug=slug)
    attending = True if request.user in this_event.users.all() else False

    return render(request, 'event.html', {'event': this_event, 'attending': attending})

@login_required(login_url='/login/')
def register(request, slug):
    this_event = get_object_or_404(Event, slug=slug)
    this_event.users.add(request.user)
    this_event.save()
    return redirect('/events/' + slug)
