from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from social.apps.django_app.views import complete as social_complete
from base.forms import InitialPassword

# todo redirect if already logged in not just blank
class Login(FormView):
    form_class = InitialPassword
    template_name = "login.html"
    success_url = 'home'

    def form_invalid(self, form):
        self.request.session.flush()
        return render(self.request, 'login.html', {'form': form, 'new_users': self.new_users})

    def form_valid(self, form):
        return social_complete(self.request, 'email')

    def get_success_url(self):
        return redirect(self.request.POST.get('next','home'))
