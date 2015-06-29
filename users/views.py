import json
from exceptions import ValueError
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.templatetags.static import static
from django.core.urlresolvers import reverse
from social.apps.django_app.default.models import UserSocialAuth
from base.views import LoginRequiredMixin
from forms import UserProfileForm

from models import UserProfile, User

class ProfileEditRedirect(RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'profile-edit-redirect'

    def get_redirect_url(self, *args, **kwargs):
        return '/users/' + self.request.user.userprofile.slug + '/edit'


class ProfileEditView(LoginRequiredMixin, FormView):
    form_class = UserProfileForm
    template_name = "profile_edit.html"
    success_url = '/'
    profile = None

    def get_initial(self):
        initial = super(ProfileEditView, self).get_initial()

        self.profile = get_object_or_404(UserProfile, user_id=self.request.user.id)

        try:
            url = self.profile.image.url
        except ValueError:
            url = static('images/avatar.jpg')

        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        initial['summary'] = self.profile.summary
        initial['country'] = self.profile.country
        initial['skills'] = [skill.id for skill in self.profile.skills.all()]
        initial['maker_type'] = [maker_type.id for maker_type in self.profile.maker_type.all()]
        initial['image_url'] = url
        initial['username'] = self.profile.user.username

        return initial

    def form_valid(self, form):
        password_changed = False
        profile_changed = False
        user_changed = False

        # todo allow email change once account link with different emails setup?
        for change in form.changed_data:
            if hasattr(self.profile, change):
                if change == 'skills':
                    through_model = self.profile.skills.through

                    # todo - probably a better way to do this
                    through_model.objects.filter(userprofile_id=self.profile.user_id).delete()

                    through_model.objects.bulk_create([through_model(skill_id=current_skill_id, userprofile_id=self.profile.user_id)
                                                      for current_skill_id in form.cleaned_data['skills']])
                else:
                    if change == 'image':
                         # remove old image form s3
                        if 'image' in form.initial:
                            form.initial['image'].delete()

                        if self.profile.thumbnail:
                            self.profile.thumbnail.delete()

                        setattr(self.profile, 'thumbnail', form.cleaned_data[change])

                    setattr(self.profile, change, form.cleaned_data[change])

                profile_changed = True

            elif hasattr(self.profile.user, change):
                if change == 'password':
                    self.profile.user.set_password(form.cleaned_data['password'])
                    password_changed = True
                else:
                    setattr(self.profile.user, change, form.cleaned_data[change])

                user_changed = True

        if profile_changed:
            self.profile.save()

        if user_changed:
            self.profile.user.save()

        if password_changed:
            return HttpResponseRedirect("/password_changed_login")

        return HttpResponseRedirect("/")

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

        # return render(self.request, 'profile_edit.html', {'form': form})
        return super(ProfileEditView, self).form_invalid(form)

def profile_view(request, slug):
    profile = get_object_or_404(UserProfile, slug=slug)

    return render(request, 'profile_view.html', {"profile": profile})


def require_email(request):
    if request.method == 'POST' and 'email' in request.POST and request.POST['email'] is not None:
        request.session['saved_email'] = request.POST.get('email')
        backend = request.session['partial_pipeline']['backend']
        return redirect('social:complete', backend=backend)

    return render_to_response('require_email.html', RequestContext(request))


def validation_sent(request):
    return render(request, 'validation_sent.html', {'email': request.session['email_validation_address']})


@login_required(redirect_field_name='/')
def delete_user(request):
    profile = get_object_or_404(UserProfile, user_id=request.user.id)
    # could use pre_delete signal here
    profile.image.delete();
    profile.delete();

    UserSocialAuth.objects.filter(user=request.user).delete()
    # don't delete in case there are some outstanding foreign keys linking to the user but set the email
    # just in case the user wants to rejoin later
    User.objects.filter(id=request.user.id).update(is_active=False, email='gone@hacklaunch.com')

    return HttpResponseRedirect('/logout')


@csrf_protect
def profile_image_upload(request):
    if request.is_ajax():
        if len(request.FILES) == 1:
            uploaded_file = request.FILES['file_data'] if request.FILES else None

            profile = request.user.userprofile
            profile.image.delete()
            profile.thumbnail.delete()
            profile.image = uploaded_file
            profile.thumbnail = uploaded_file
            profile.save()

            return HttpResponse(json.dumps({'success': True, 'thumbnailUrl': profile.thumbnail.url}))
        else:
            return HttpResponseBadRequest(json.dumps({'success': False, 'message': 'Multiple file uploaded'}))

    return HttpResponseBadRequest(json.dumps({'success': False, 'message': 'Invalid request'}))


@csrf_protect
def get_user(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'username' in request.POST:
                username = request.POST['username']

                if len(username) == 0:
                    return HttpResponseBadRequest(json.dumps({'success': False, 'message': 'No username in request'}))

                if username[0] is '@':
                    username = username[1:]

                profile = UserProfile.objects.get(user__username=username)

                if not profile:
                    return HttpResponseBadRequest(json.dumps({'success': False, 'message': 'No user with username: ' + username}))

                if not profile.thumbnail:
                    thumbnail = static('images/avatar.jpg')
                else:
                    thumbnail = profile.thumbnail.url

                return HttpResponse(json.dumps({'success': True, 'username': username, 'full_name': profile.user.get_full_name(),
                                                'thumbnail': thumbnail, 'slug': profile.slug}))
            else:
                return HttpResponseBadRequest(json.dumps({'success': False, 'message': 'No username in request'}))

    return HttpResponseBadRequest(json.dumps({'success': False, 'message': 'Invalid request'}))
