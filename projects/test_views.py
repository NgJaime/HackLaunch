import json

from django.test import RequestFactory
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from freezegun import freeze_time
from test_plus.test import TestCase
from django.test import TestCase as StandardTestCase

from datetime import datetime, timedelta

from projects.models import Project, ProjectCreator, Follower, Views, ProjectCreatorInitialisation
from users.models import Skill, User, UserProfile
from users.user_activity_models import UserActivity
from projects.views import ProjectListView, get_project_context, project_ajax_request, UserProjectsListView


class ProjectListViewTestCase(TestCase):

    def test_get_queryset(self):
        project = Project.objects.create(title='<p>title</p>')

        project_list = ProjectListView()

        projects = project_list.get_queryset()

        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0], project)

    def test_get_context_data(self):
        project = Project.objects.create(title='<p>title</p>')
        project_views_yesterday = Views.objects.create(project=project, count=10, date=datetime.now() - timedelta(hours=24))
        project_views_today = Views.objects.create(project=project, count=20, date=datetime.now())
        project_views_tomorrow = Views.objects.create(project=project, count=30, date=datetime.now() + timedelta(hours=24))

        request = RequestFactory().get('/fake-path')
        view = ProjectListView.as_view()
        response = view(request)

        self.assertEqual(len(response.context_data['popular_projects']), 1)
        self.assertEqual(response.context_data['popular_projects'][0].project.id, project.id)
        self.assertEqual(response.context_data['popular_projects'][0].count, project_views_yesterday.count)


class UserProjectsListViewTestCase(TestCase):

    def test_get_queryset_one_expected_object(self):
        user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        user_profile = UserProfile.objects.create(user=user)
        project = Project.objects.create(title='<p>title</p>')
        project_creator = ProjectCreator.objects.create(creator=user, project=project)

        url = self.reverse('user_projects', slug=user_profile.slug)
        self.get(url)

        self.response_200()

        self.assertEqual(len(self.context['project_creator']), 1)
        self.assertEqual(self.context['project_creator'][0], project_creator)

    def test_get_queryset_non_query_match_in_db(self):
        user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        user_profile = UserProfile.objects.create(user=user)
        project = Project.objects.create(title='<p>title</p>')
        project_creator = ProjectCreator.objects.create(creator=user, project=project)

        user2 = User.objects.create_user('someone2', 'someone2@somewhere.com', 'password')
        user_profile2 = UserProfile.objects.create(user=user2)
        project2 = Project.objects.create(title='<p>title2</p>')

        url = self.reverse('user_projects', slug=user_profile.slug)
        self.get(url)

        self.response_200()

        self.assertEqual(len(self.context['project_creator']), 1)
        self.assertEqual(self.context['project_creator'][0], project_creator)

    def test_followers_in_context(self):
        user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        user_profile = UserProfile.objects.create(user=user)
        project = Project.objects.create(title='<p>title</p>')
        project_creator = ProjectCreator.objects.create(creator=user, project=project)

        user2 = User.objects.create_user('someone2', 'someone2@somewhere.com', 'password')
        user_profile2 = UserProfile.objects.create(user=user2)
        project2 = Project.objects.create(title='<p>title2</p>')

        following = Follower.objects.create(project=project, user=user)
        following_other = Follower.objects.create(project=project2, user=user2)

        url = self.reverse('user_projects', slug=user_profile.slug)
        self.get(url)

        self.response_200()

        self.assertEqual(len(self.context['following']), 1)
        self.assertEqual(self.context['following'][0], following)

    def test_user_in_context(self):
        user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        user_profile = UserProfile.objects.create(user=user)
        project = Project.objects.create(title='<p>title</p>')
        project_creator = ProjectCreator.objects.create(creator=user, project=project)

        url = self.reverse('user_projects', slug=user_profile.slug)
        self.get(url)

        self.response_200()

        self.assertEqual(self.context['user'], user_profile.slug)

class ProjectViewTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def test_get_context_data_anonymous_user(self):
        url = self.reverse('project_view', slug='hacklaunch-2015')
        self.get(url)

        self.response_200()

        self.assertFalse(self.context['follower'])
        self.assertTrue(self.context['prior_creators'])
        self.assertEqual(self.context['project'].id, 59)
        self.assertEqual(len(self.context['technologies']), 2)
        self.assertEqual(len(self.context['posts']), 3)
        self.assertEqual(len(self.context['creators']), 2)
        self.assertFalse(self.context['project_admin'])

        views = Views.objects.filter(project=self.context['project'], date=datetime.date(datetime.now()))
        self.assertEqual(len(views), 1)

    def test_get_context_data_user_following(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        project = Project.objects.get(slug='hacklaunch-2015')
        follower = Follower.objects.create(user=self.user, project=project)

        url = self.reverse('project_view', slug='hacklaunch-2015')
        self.get(url)

        self.response_200()

        self.assertTrue(self.context['follower'])
        self.assertTrue(self.context['prior_creators'])
        self.assertEqual(self.context['project'].id, 59)
        self.assertEqual(len(self.context['technologies']), 2)
        self.assertEqual(len(self.context['posts']), 3)
        self.assertEqual(len(self.context['creators']), 2)
        self.assertFalse(self.context['project_admin'])

        views = Views.objects.filter(project=self.context['project'], date=datetime.date(datetime.now()))
        self.assertEqual(len(views), 1)

    def test_get_context_data_user_is_admin(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        project = Project.objects.get(slug='hacklaunch-2015')

        project_creator = ProjectCreator.objects.create(creator=self.user, project=project, is_active=True,
                                                        is_admin=True, awaiting_confirmation=False)

        url = self.reverse('project_view', slug='hacklaunch-2015')
        self.get(url)

        self.response_200()

        self.assertFalse(self.context['follower'])
        self.assertTrue(self.context['prior_creators'])
        self.assertEqual(self.context['project'].id, 59)
        self.assertEqual(len(self.context['technologies']), 2)
        self.assertEqual(len(self.context['posts']), 3)
        self.assertEqual(len(self.context['creators']), 3)
        self.assertTrue(self.context['project_admin'])

        views = Views.objects.filter(project=self.context['project'], date=datetime.date(datetime.now()))
        self.assertEqual(len(views), 1)


@freeze_time("2012-01-01")
class GetProjectContextTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')

    def test_context(self):
        Skill.objects.create(name='something')
        project = Project.objects.create()

        context = get_project_context(project)

        self.assertEqual(context['date'], '01/01/2012')
        self.assertEqual(context['month'], 'January')
        self.assertEqual(context['projectId'], project.id)
        self.assertEqual(context['technologies'], '["something"]')

    def test_context_with_active_creator(self):
        Skill.objects.create(name='something')
        project = Project.objects.create()
        ProjectCreator.objects.create(project=project, creator=self.user, is_active=True)

        context = get_project_context(project)

        self.assertEqual(context['date'], '01/01/2012')
        self.assertEqual(context['month'], 'January')
        self.assertEqual(context['projectId'], project.id)
        self.assertEqual(context['technologies'], '["something"]')
        self.assertEqual(context['prior_creator'], False)

    def test_context_with_prior_creator(self):
        Skill.objects.create(name='something')
        project = Project.objects.create()
        ProjectCreator.objects.create(project=project, creator=self.user, is_active=False)

        context = get_project_context(project)

        self.assertEqual(context['date'], '01/01/2012')
        self.assertEqual(context['month'], 'January')
        self.assertEqual(context['projectId'], project.id)
        self.assertEqual(context['technologies'], '["something"]')
        self.assertEqual(context['prior_creator'], True)


class ProjectEditTestCase(TestCase):

    def tearDown(self):
        self.client.logout()

        if self.projectCreator:
            self.projectCreator.delete()
        self.user.delete()
        self.project.delete()

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')
        self.project = Project.objects.create(title='<p>awesome-project</p>', is_active=True)
        self.projectCreator = ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

    def test_login_required(self):
        self.client.logout()

        self.post('project_edit' , slug='awesome-project')

        self.response_302()
        self.assertEqual(self.last_response.url, 'http://testserver/login?next=/projects/awesome-project/edit/')

    def test_post_request_request(self):
        self.post('project_edit' , slug='awesome-project')
        self.response_404()

    @freeze_time("2012-01-01")
    def test_get_valid_project_user_is_admin(self):
        url = self.reverse('project_edit', slug='awesome-project')
        self.get(url)

        self.response_200()

        self.assertEqual(len(Project.objects.all()), 1)
        self.assertEqual(len(ProjectCreator.objects.all()), 1)

        self.assertEqual(self.context['project'].id, Project.objects.all()[0].id)
        self.assertEqual(self.context['context']['projectId'], Project.objects.all()[0].id)
        self.assertEqual(self.context['context']['month'], 'January')
        self.assertEqual(self.context['context']['date'], '01/01/2012')
        self.assertEqual(self.context['project_tags'], '')
        self.assertEqual(len(self.context['project_technologies']), 0)

    def test_get_valid_project_user_not_admin(self):
        self.projectCreator.delete()
        self.projectCreator = ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=False)

        url = self.reverse('project_edit', slug='awesome-project')
        self.get(url)

        self.response_302()
        self.assertEqual(self.last_response.url, 'http://testserver/projects/awesome-project')

    def test_invalid_slug(self):
        url = self.reverse('project_edit', slug='not-a-project-slug')
        self.get(url)

        self.response_404()

    def test_invalid_creator(self):
        self.projectCreator.delete()
        self.projectCreator = None

        url = self.reverse('project_edit', slug='awesome-project')
        self.get(url)

        self.response_302()
        self.assertEqual(self.last_response.url, 'http://testserver/projects/awesome-project')


class FollowProjectTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

    def test_add_follower(self):
        number_followers = len(Follower.objects.all())
        self.assertEqual(number_followers, 0)

        url = self.reverse('follow_project')
        xml_response = self.post(url, extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}, data={'project': '59', 'follow': 'true'})

        number_followers = len(Follower.objects.all())
        self.assertEqual(number_followers, 1)

        follower = Follower.objects.get(project_id=59, user_id=self.user.id)

    def test_remove_follower(self):
        project = Project.objects.get(id=59)
        Follower.objects.create(project=project, user=self.user)

        number_followers = len(Follower.objects.all())
        self.assertEqual(number_followers, 1)

        url = self.reverse('follow_project')
        xml_response = self.post(url, extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}, data={'project': '59', 'follow': 'false'})

        number_followers = len(Follower.objects.all())
        self.assertEqual(number_followers, 0)

    def test_login_required(self):
        self.client.logout()
        project = Project.objects.get(id=59)

        url = self.reverse('follow_project')
        xml_response = self.post(url, extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}, data={'project': '59', 'follow': 'false'})

        self.response_200()
        self.assertEqual(xml_response.content, '{"status": 401, "message": "Login required"}')



@freeze_time("2012-01-01")
class ProjectCreateTestCase(TestCase):
    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

    def test_post_request_request(self):
        response = self.client.post(reverse('project_create'))

        self.assertEqual(response.status_code, 404)

    def test_get_request(self):
        self.assertEqual(len(Project.objects.all()), 0)
        self.assertEqual(len(ProjectCreator.objects.all()), 0)

        response = self.client.get(reverse('project_create'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Project.objects.all()), 1)
        self.assertEqual(len(ProjectCreator.objects.all()), 1)
        self.assertEqual(response.context[0].dicts[2]['context']['projectId'], Project.objects.all()[0].id)
        self.assertEqual(response.context[0].dicts[2]['context']['month'], 'January')
        self.assertEqual(response.context[0].dicts[2]['context']['date'], '01/01/2012')
        self.assertEqual(response.context[0].dicts[2]['project_tags'], [])
        self.assertEqual(response.context[0].dicts[2]['project_technologies'], [])


class ProjectValidateCreatorTestCase(TestCase):

    def test_post_request_request(self):
        response = self.client.get(reverse('validate_creator', kwargs={'code': 'none'}))
        self.assertEqual(response.status_code, 404)

    def test_get_request(self):
        user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        project = Project.objects.create(title='<p>title</p>')
        project_creator = ProjectCreator.objects.create(creator=user, project=project)

        ProjectCreatorInitialisation.objects.create(code='1234', creator=project_creator, date_added=datetime.now())

        response = self.client.get(reverse('validate_creator', kwargs={'code': '1234'}))

        user_activity = UserActivity.objects.get(user=user,
                                                 project=project,
                                                 event_type=UserActivity.JOINED_PROJECT_EVENT)

        initialisation = ProjectCreatorInitialisation.objects.filter(code='1234', creator=ProjectCreator)

        self.assertIsNotNone(user_activity)
        self.assertEqual(len(initialisation), 0)
