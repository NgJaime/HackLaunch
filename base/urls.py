"""urlconf for the base application"""

from django.conf.urls import url, patterns
from . import views


urlpatterns = [url(r'^terms/$', views.terms, name='terms'),
               url(r'^$', views.HomeView.as_view(), name='home')]
