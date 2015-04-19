from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import User


def home(request):
    # todo this should be cached
    new_users = User.objects.order_by('date_joined')[:10]

    context = {
        'new_users': new_users
    }

    return render(request, 'home.html', context)


def terms(request):
    return render(request, 'terms.html')


def credits(request):
    return render(request, 'credits.html')


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
