from django.shortcuts import render
from base.forms import InitialPassword

def home(request):
    data = {
        'form': InitialPassword(),
    }

    return render(request, 'home.html', data)
