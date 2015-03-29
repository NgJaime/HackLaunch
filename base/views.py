from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from base.forms import InitialPassword


def home(request):
    return render(request, 'home.html', {'form': InitialPassword()})


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
