from django.conf.urls import include, url
from django.contrib import admin

# todo remove debug
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    url(r'^$', 'base.views.home'),

    url(r'^profile/$', 'users.views.profile_edit', name='profile_edit'),
    url(r'^profile/(?P<slug>[^/]+)/$', 'users.views.profile_view', name='profile_view'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^email/$', 'users.views.require_email', name='require_email'),
    url(r'^validation_sent/$', 'users.views.validation_sent', name='validation_sent'),
    url(r'^email_complete/$', 'users.views.email_complete', name='email_complete'),

    url(r'^login/$', 'base.views.home'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'registration/password_change_form.html'}, name='password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done',
        {'template_name': 'registration/password_change_done.html'}, name='password_change_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'registration/password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'registration/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
