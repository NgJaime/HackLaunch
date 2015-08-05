from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from projects.ajax_decorators import ajax_login_required
from . import views


urlpatterns = [ url(r'list/$', views.ProjectListView.as_view(), name='project_list'),
                url(r'user/(?P<slug>[^/]+)$', views.UserProjectsListView.as_view(), name='user_projects'),

                url(r'image_upload/$', ajax_login_required(views.image_upload), name='project_image_upload'),
                url(r'image_delete/$', ajax_login_required(views.image_delete), name='project_image_delete'),
                url(r'update_project/$', ajax_login_required(views.update_project), name='update_project'),
                url(r'update_repo/$', ajax_login_required(views.update_repo), name='update_repo'),
                url(r'add_post/$', ajax_login_required(views.add_post), name='add_post'),
                url(r'update_post/$', ajax_login_required(views.update_post), name='update_post'),
                url(r'addCreator/$', ajax_login_required(views.add_creator), name='add_creator_to_project'),
                url(r'removeCreator/$', ajax_login_required(views.remove_creator), name='remove_creator_from_project'),
                url(r'updateCreator/$', ajax_login_required(views.update_creator), name='update_creator'),
                url(r'addTechnology/$', ajax_login_required(views.add_technology), name='add_technology_to_project'),
                url(r'removeTechnology/$', ajax_login_required(views.remove_technology), name='remove_technology_from_project'),
                url(r'updateTechnology/$', ajax_login_required(views.update_technology), name='update_project_technology'),
                url(r'addTag/$', ajax_login_required(views.add_tag), name='add_tag_to_project'),
                url(r'removeTag/$', ajax_login_required(views.remove_tag), name='remove_tag_from_project'),
                url(r'followProject/$', ajax_login_required(views.follow_project), name='follow_project'),

                url(r'^(?P<slug>[^/]+)$', views.ProjectView.as_view(), name='project_view'),
                url(r'^(?P<slug>[^/]+)/(?P<post>[^/]+)$', views.ProjectPostView.as_view(), name='project_post_view'),
                url(r'^(?P<slug>[^/]+)/edit/$', login_required(views.project_edit), name='project_edit'),
                url(r'create/$', login_required(views.project_create), name='project_create'),
                url(r'validate_creator/(?P<code>[^/]+)$', views.validate_creator, name='validate_creator')]
