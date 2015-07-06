import json

from django.test import RequestFactory
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from freezegun import freeze_time
from test_plus.test import TestCase
from django.test import TestCase as StandardTestCase

from projects.models import Project, ProjectCreator, Follower
from users.models import Skill, User
from projects.views import PostListView, get_project_context, project_ajax_request


class PostListViewTestCase(TestCase):

    def test_get_queryset(self):
        project = Project.objects.create(title='<p>title</p>')
        project.save()

        post_list = PostListView()

        projects = post_list.get_queryset()

        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0], project)


class ProjectViewTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def test_get_context_data_anonymous_user(self):
        url = self.reverse('project_view', slug='hacklaunch-2015')
        self.get(url)

        self.response_200()

        self.assertFalse(self.context['follower'])
        self.assertEqual(self.context['project'].id, 59)
        self.assertEqual(len(self.context['technologies']), 2)
        self.assertEqual(len(self.context['posts']), 3)


class GetProjectContextTestCase(TestCase):
    @freeze_time("2012-01-01")
    def test_context(self):
        Skill.objects.create(name='something')
        project_id = '1'

        context = get_project_context(project_id)

        self.assertEqual(context['date'], '01/01/2012')
        self.assertEqual(context['month'], 'January')
        self.assertEqual(context['projectId'], project_id)
        self.assertEqual(context['technologies'], '["something"]')


class ProjectEditTestCase(TestCase):

    def tearDown(self):
        self.client.logout()
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

        url = self.reverse('follow_project')
        xml_response = self.post(url, extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}, data={'project': '59', 'follow': 'false'})

        self.response_302()
        self.assertEqual(xml_response.url, 'http://testserver/login?next=/projects/followProject/')



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
