from django.conf.urls import url, patterns
from . import views


urlpatterns = [url(r'innovate-or-die/$', views.event, name='innovate-or-die')]
