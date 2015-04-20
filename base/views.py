from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from social.apps.django_app.views import complete as social_complete
from users.models import User
from base.forms import InitialPassword

class HomeView(FormView):
    form_class = InitialPassword
    template_name = "home.html"
    success_url = 'profile_edit'
    new_users = User.objects.order_by('date_joined')[:10]

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['new_users'] = self.new_users
        return self.render_to_response(context)

    def form_invalid(self, form):
        self.request.session.flush()

        return render(self.request, 'home.html', {'form': form, 'new_users': self.new_users})


    def form_valid(self, form):
        return social_complete(self.request, 'email')


def terms(request):
    return render(request, 'terms.html')


def credits(request):
    return render(request, 'credits.html')


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
