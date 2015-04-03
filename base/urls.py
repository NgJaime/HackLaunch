"""urlconf for the base application"""

from django.conf.urls import url, patterns
from . import views


urlpatterns = [url(r'^terms/$', views.terms),
               url(r'^$', views.home)]
