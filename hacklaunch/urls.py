from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from base.sitemap import StaticViewSitemap, ProfileSitemap, EventsSitemap
from auth.views import Login, logout, PasswordChangedLogin

admin.autodiscover()

sitemaps = {
    'static': StaticViewSitemap,
    'events': EventsSitemap,
    'profiles': ProfileSitemap,
}

urlpatterns = [
    url(r'^$', include('base.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^users/', include('users.urls')),

    url(r'^terms/$', 'base.views.terms', name='terms'),
    url(r'^credits/$', 'base.views.credits', name='credits'),

    url(r'^robots\.txt/$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^email_required/$', 'users.views.require_email', name='require_email'),
    url(r'^validation_sent/$', 'users.views.validation_sent', name='validation_sent'),
    url(r'^complete/(?P<backend>[^/]+)/$', 'auth.views.complete', name='complete'),

    url(r'^logout/$', login_required(logout), name='logout'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^password_changed_login/$', PasswordChangedLogin.as_view(), name='password_changed_login'),

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

    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^search/', include('haystack.urls'), name='search')
]

from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
