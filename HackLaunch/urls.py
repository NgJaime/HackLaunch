from django.conf.urls import include, url
from django.contrib import admin

# todo remove debug
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    url(r'^$', 'base.views.home'),

    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^profile/$', 'users.views.profile', name='profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^email/$', 'users.views.require_email', name='require_email'),
    url(r'^validation_sent/$', 'users.views.validation_sent', name='validation_sent'),
    url(r'^email_complete/$', 'users.views.email_complete', name='email_complete'),



    url(r'', include('social.apps.django_app.urls', namespace='social'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
