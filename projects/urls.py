from django.conf.urls import url, patterns
from . import views


urlpatterns = [url(r'project/edit$', views.ProjectEditView.as_view(), name='project_edit'),
               url(r'project/$', views.project, name='project')]
