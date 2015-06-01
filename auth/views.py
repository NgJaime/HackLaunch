from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from social.apps.django_app.views import complete as social_complete
from base.forms import InitialPassword

# todo redirect if already logged in not just blank
class Login(FormView):
    form_class = InitialPassword
    template_name = "login.html"
    success_url = 'home'

    def form_invalid(self, form):
        return render(self.request, 'login.html', {'form': form})

    def form_valid(self, form):
        if 'email_validation_address' in self.request.session:
            self.request.session.pop('email_validation_address')

            if 'partial_pipeline' in self.request.session \
                and 'backend' in self.request.session['partial_pipeline'] \
                and self.request.session['partial_pipeline']['backend'] == u'email':
                self.request.session.pop('partial_pipeline')

        return social_complete(self.request, 'email')

    def get_success_url(self):
        return redirect(self.request.POST.get('next','home'))


def complete(request, backend, *args, **kwargs):

    if request.method == 'POST' and backend == u'email':
        form = InitialPassword(request.POST)

        if form.is_valid():
            if 'email_validation_address' in request.session:
                request.session.pop('email_validation_address')

                if 'partial_pipeline' in request.session \
                    and 'backend' in request.session['partial_pipeline'] \
                    and request.session['partial_pipeline']['backend'] == u'email':
                    request.session.pop('partial_pipeline')
        else:
            return render(request, 'home.html', {'form': form})

    return social_complete(request, backend, *args, **kwargs)


# todo refactor with login above
class PasswordChangedLogin(FormView):
    form_class = InitialPassword
    template_name = "password_changed_login.html"
    success_url = 'home'

    def form_invalid(self, form):
        return render(self.request, 'password_changed_login.html', {'form': form})

    def form_valid(self, form):
         if 'email_validation_address' in self.request.session:
            self.request.session.pop('email_validation_address')

            if 'partial_pipeline' in self.request.session \
                and 'backend' in self.request.session['partial_pipeline'] \
                and self.request.session['partial_pipeline']['backend'] == u'email':
                self.request.session.pop('partial_pipeline')

         return social_complete(self.request, 'email')

    def get_success_url(self):
        return redirect(self.request.POST.get('next','home'))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
