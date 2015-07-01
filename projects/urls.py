from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [ url(r'list/$', views.PostListView.as_view(), name='project_list'),

                url(r'image_upload/$', login_required(views.image_upload), name='project_image_upload'),
                url(r'image_delete/$', login_required(views.image_delete), name='project_image_delete'),
                url(r'update_project/$', login_required(views.update_project), name='update_project'),
                url(r'add_post/$', login_required(views.add_post), name='add_post'),
                url(r'update_post/$', login_required(views.update_post), name='update_post'),
                url(r'addCreator/$', login_required(views.add_creator), name='add_creator_to_project'),
                url(r'removeCreator/$', login_required(views.remove_creator), name='remove_creator_from_project'),
                url(r'updateCreator/$', login_required(views.update_creator), name='update_creator'),
                url(r'addTechnology/$', login_required(views.add_technology), name='add_technology_to_project'),
                url(r'removeTechnology/$', login_required(views.remove_technology), name='remove_technology_from_project'),
                url(r'addTag/$', login_required(views.add_tag), name='add_tag_to_project'),
                url(r'removeTag/$', login_required(views.remove_tag), name='remove_tag_from_project'),
                url(r'followProject/$', login_required(views.follow_project), name='follow_project'),

                url(r'^(?P<slug>[^/]+)$', views.ProjectView.as_view(), name='profile_view'),
                url(r'^(?P<slug>[^/]+)/edit/$', login_required(views.project_edit), name='project_edit'),
                url(r'create/$', login_required(views.project_create), name='project_create')]
