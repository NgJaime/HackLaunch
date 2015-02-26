from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', include('base.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^register/$', 'users.views.register', name='register'),
    url(r'^admin/', include(admin.site.urls)),

    url('', include('social.apps.django_app.urls', namespace='social')),
]
