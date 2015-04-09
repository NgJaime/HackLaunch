from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from base.forms import InitialPassword
from social.apps.django_app.views import complete as social_complete
from forms import UserProfileForm
from models import UserProfile, User
from social.apps.django_app.default.models import UserSocialAuth
from base.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class ProfileEditView(LoginRequiredMixin, FormView):
    form_class = UserProfileForm
    template_name = "profile_edit.html"
    success_url = '/'
    profile = None

    def get_initial(self):
        initial = super(ProfileEditView, self).get_initial()

        self.profile, created = UserProfile.objects.get_or_create(user_id=self.request.user.id)

        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        initial['summary'] = self.profile.summary
        initial['location'] = self.profile.location
        initial['skills'] = [skill.id for skill in self.profile.skills.all()]
        initial['maker_type'] = [maker_type.id for maker_type in self.profile.maker_type.all()]
        initial['image'] = self.profile.image
        initial['username'] = self.profile.user.username

        return initial

    def form_valid(self, form):
        # todo allow email change once account link with different emails setup
        for change in form.changed_data:
            if hasattr(self.profile, change):
                if change == 'skills':
                    throughModel = self.profile.skills.through

                    # todo - probably a better way to do this
                    throughModel.objects.filter(userprofile_id=self.profile.user_id).delete()

                    throughModel.objects.bulk_create([throughModel(skill_id=current_skill_id, userprofile_id=self.profile.user_id)
                                                      for current_skill_id in form.cleaned_data['skills']])
                else:
                    # remove old image form s3
                    if change == 'image' and 'image' in form.initial:
                        form.initial['image'].delete()

                    setattr(self.profile, change, form.cleaned_data[change])

            elif hasattr(self.profile.user, change):
                if change == 'password':
                    self.profile.user.set_password(form.cleaned_data['password'])
                    send_password_changed_email(self.profile.user)

                else:
                    setattr(self.profile.user, change, form.cleaned_data[change])

            # we now have all of the required fields
            self.profile.user.minimalProfile = True

            self.profile.save()
            self.profile.user.save()

        return render(self.request, 'home.html')

    def form_invalid(self, form):
        if self.request.user.nonSocialAuth is False \
            and 'password' in form.errors \
            and 'password_confirmation' in form.errors \
            and len(form.errors['password']) == 1 \
            and form.errors['password'][0] == u'This field is required.'\
            and len(form.errors['password_confirmation']) == 1 \
            and form.errors['password_confirmation'][0] == u'This field is required.':

                form.errors.pop('password', None)
                form.errors.pop('password_confirmation', None)

        if len(form.errors) == 0:
            return self.form_valid(form)

        return render(self.request, 'profile_edit.html', {'form': form})


def send_password_changed_email(user):
    context = {
        'first_name': user.first_name,
        'email': user.email
    }

    html_message = get_template('password_changed_email.html').render(Context(context))
    email = EmailMessage('Your password at HackLaunch has been changed', html_message, to=[user.email], from_email=settings.EMAIL_FROM)
    email.content_subtype = 'html'
    email.send()


def profile_view(request, slug):
    profile = get_object_or_404(UserProfile, slug=slug)

    return render(request, 'profile_view.html', {"profile": profile})


def require_email(request):
    if request.method == 'POST':
        request.session['saved_email'] = request.POST.get('email')
        backend = request.session['partial_pipeline']['backend']
        return redirect('social:complete', backend=backend)
    return render_to_response('email.html', RequestContext(request))


def validation_sent(request):
    return render(request, 'validation_sent.html', {'email': request.session['email_validation_address']})


def email_complete(request):
    return render(request, 'email_complete.html')


def complete(request, backend, *args, **kwargs):

    if request.method == 'POST' and backend == u'email':
        form = InitialPassword(request.POST)

        if not form.is_valid():
            return render(request, 'home.html', {'form': form})

    return social_complete(request, backend, *args, **kwargs)

@login_required(redirect_field_name='/')
def delete_user(request):
    profile = get_object_or_404(UserProfile, user_id=request.user.id)
    # could use pre_delete signal here
    profile.image.delete();
    profile.delete();

    UserSocialAuth.objects.filter(user=request.user).delete()
    # don't delete in case there are some outstanding foreign keys linking to the user but set the email
    # just in case the user wants to rejoin later
    User.objects.filter(id=request.user.id).update(is_active=False, email='gone@hacklaaunch.com')

    return HttpResponseRedirect(reverse('django.contrib.auth.views.logout'))


