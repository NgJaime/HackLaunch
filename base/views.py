from django.shortcuts import render


def home(request):
    """ Default view for the root """
    return render(request, 'home.html')
