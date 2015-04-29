from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from social.apps.django_app.views import complete as social_complete
from users.models import User
from base.forms import InitialPassword


class HomeView(FormView):
    form_class = InitialPassword
    template_name = "home.html"
    success_url = 'profile_edit'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        new_users = User.objects.order_by('-date_joined')[:10]
        context['new_users'] = new_users
        context['form'] = self.form_class
        return self.render_to_response(context)

    def form_invalid(self, form):
        self.request.session.flush()
        new_users = User.objects.order_by('-date_joined')[:10]
        return render(self.request, 'home.html', {'form': form, 'new_users': new_users})

    def form_valid(self, form):
        return social_complete(self.request, 'email')


def terms(request):
    return render(request, 'terms.html')


def credits(request):
    return render(request, 'credits.html')

# todo move to auth
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
