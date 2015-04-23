from django.conf.urls import include, url
from django.contrib import admin
from users.views import ProfileEditView

admin.autodiscover()

urlpatterns = [
    url(r'^$', include('base.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^terms/$', 'base.views.terms', name='terms'),
    url(r'^credits/$', 'base.views.credits', name='credits'),

    url(r'^profile/$', ProfileEditView.as_view()),
    url(r'^profile/(?P<slug>[^/]+)/$', 'users.views.profile_view', name='profile_view'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^email_required/$', 'users.views.require_email', name='require_email'),
    url(r'^validation_sent/$', 'users.views.validation_sent', name='validation_sent'),

    url(r'^logout/$', 'users.views.logout', name='logout'),
    url(r'^delete_user/$', 'users.views.delete_user'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'password_reset_form.html', 'html_email_template_name': 'password_reset_email.html'}, name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'password_reset_complete.html'}, name='password_reset_complete'),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
]

from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
