from django.shortcuts import render
from base.forms import InitialPassword

def home(request):
    context = {
        'form': InitialPassword(),
    }

    return render(request, 'home.html', context)
