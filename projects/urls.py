from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
                # url(r'project/edit$', views.ProjectEditView.as_view(), name='project_edit'),
                url(r'project/edit$', login_required(views.projectEdit), name='project_edit'),
                url(r'project/create', login_required(views.projectCreate), name='project_create'),
                url(r'project/$', views.ProjectView.as_view(), name='project'),
                url(r'addCreator/$', login_required(views.addCreator), name='add_creator_to_project'),
                url(r'addTechnology/$', login_required(views.add_technology), name='add_technology_to_project'),
                url(r'removeTechnology/$', login_required(views.remove_technology), name='remove_technology_from_project')]
