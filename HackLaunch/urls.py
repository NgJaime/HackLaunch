from django.conf.urls import include, url
from django.contrib import admin

# todo remove debug
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    url(r'^$', 'base.views.home'),

    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^register/$', 'users.views.register', name='register'),
    url(r'^profile/$', 'users.views.profile', name='profile'),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^complete/email/', include('base.urls')),

    url(r'', include('social.apps.django_app.urls', namespace='social'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
