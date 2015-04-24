from django.conf.urls import url, patterns
from . import views


urlpatterns = [url(r'(?P<slug>[^/]+)/register$', views.register, name='register'),
               url(r'(?P<slug>[^/]+)/$', views.event, name='event')]


