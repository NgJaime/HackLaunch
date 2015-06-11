from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from users.views import ProfileEditView, profile_image_upload, get_user


urlpatterns = [url(r'^(?P<slug>[^/]+)/edit$', login_required(ProfileEditView.as_view())),
               url(r'^(?P<slug>[^/]+)/$', 'users.views.profile_view', name='profile_view'),
               url(r'^upload/profile_image', login_required(profile_image_upload), name='profile_image_upload'),
               url(r'^get_user', login_required(get_user), name='get_user')]
