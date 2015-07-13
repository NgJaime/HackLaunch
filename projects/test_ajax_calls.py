import json
from django.test import RequestFactory
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import AnonymousUser
from mock import MagicMock, patch
from test_plus.test import TestCase

from users.models import User
from projects.models import ProjectCreator, Project, Post, Technologies, ProjectTechnologies
from freezegun import freeze_time

from projects.views import add_post, update_project, update_post, image_upload, add_creator, remove_creator, \
                           update_creator, add_technology, remove_technology, update_technology, add_tag, remove_tag, \
                           project_ajax_request


@freeze_time("2012-01-01")
class AddPostTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.factory = RequestFactory()

        # todo this ideally should be mocked by patching project_ajax_request
        self.project = Project.objects.get(id=59)
        ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

        self.request = self.factory.post('/test/', content_type='application/json')
        self.request._dont_enforce_csrf_checks = True
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.request.POST = self.request.POST.copy()
        self.request.POST = {'project': '59'}
        self.request.user = self.user

    def test_new_post(self):
        start_post_count = Post.objects.count()
        response = add_post(self.request)
        end_post_count = Post.objects.count()

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"post_id": 49, "month": "January", "success": true, "date_added": "01/01/2012"}}')
        self.assertEqual(start_post_count, end_post_count - 1)


@freeze_time("2012-01-01")
class UpdateProjectTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def setUp(self):
        # todo this ideally should be mocked by patching project_ajax_request
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.project = Project.objects.get(id=59)
        ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

        self.factory = RequestFactory()
        self.request = self.factory.post('/test/', content_type='application/json')
        self.request._dont_enforce_csrf_checks = True
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.request.POST = self.request.POST.copy()
        self.request.user = self.user

    def test_data_not_in_post(self):
        self.request.POST = {'project': '59'}

        response = update_project(self.request)
        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "No data in request", "success": false}}')

    def test_field_not_in_post(self):
        self.request.POST = {'project': '59', 'data': '{"somethign": "nothing"}'}

        response = update_project(self.request)
        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "No field in request", "success": false}}')

    def test_update_pitch(self):
        self.request.POST = {'project': '59', 'data': '{"field": "pitch"}', 'body': 'test pitch'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        project = Project.objects.get(id=59)
        self.assertEqual(project.pitch, 'test pitch')

    def test_update_tagline(self):
        self.request.POST = {'project': '59', 'data': '{"field": "tagline"}', 'body': 'test tagline'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        project = Project.objects.get(id=59)
        self.assertEqual(project.tag_line, 'test tagline')

    def test_update_title(self):
        self.request.POST = {'project': '59', 'data': '{"field": "title"}', 'body': 'test title'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        project = Project.objects.get(id=59)
        self.assertEqual(project.title, 'test title')

    def test_update_valid_facebook(self):
        self.request.POST = {'project': '59', 'data': '{"field": "facebook", "value": "www.facebook.com/test"}'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        project = Project.objects.get(id=59)
        self.assertEqual(project.facebook, 'http://www.facebook.com/test')

    def test_update_valid_google_plus(self):
        self.request.POST = {'project': '59', 'data': '{"field": "google-plus", "value": "www.plus.google.com/test"}'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        project = Project.objects.get(id=59)
        self.assertEqual(project.google_plus, 'http://www.plus.google.com/test')

    def test_update_valid_instagram(self):
        self.request.POST = {'project': '59', 'data': '{"field": "instagram", "value": "www.instagram.com/test"}'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        project = Project.objects.get(id=59)
        self.assertEqual(project.instagram, 'http://www.instagram.com/test')

    def test_update_valid_pinterest(self):
        self.request.POST = {'project': '59', 'data': '{"field": "pinterest", "value": "www.pinterest.com/test"}'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        project = Project.objects.get(id=59)
        self.assertEqual(project.pinterest, 'http://www.pinterest.com/test')

    def test_update_valid_twitter_www(self):
        self.request.POST = {'project': '59', 'data': '{"field": "twitter", "value": "www.twitter.com/test"}'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        project = Project.objects.get(id=59)
        self.assertEqual(project.twitter, 'http://www.twitter.com/test')

    def test_update_valid_http(self):
        self.request.POST = {'project': '59', 'data': '{"field": "twitter", "value": "http://www.twitter.com/test"}'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        project = Project.objects.get(id=59)
        self.assertEqual(project.twitter, 'http://www.twitter.com/test')

    def test_update_valid_https(self):
        self.request.POST = {'project': '59', 'data': '{"field": "twitter", "value": "https://www.twitter.com/test"}'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        project = Project.objects.get(id=59)
        self.assertEqual(project.twitter, 'https://www.twitter.com/test')

    def test_update_invalid_url_ending(self):
        self.request.POST = {'project': '59', 'data': '{"field": "twitter", "value": "https://www.twitter.com"}'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Invalid social media link", "success": false}}')

    def test_update_invalid_url_ending_trailing_slash(self):
        self.request.POST = {'project': '59', 'data': '{"field": "twitter", "value": "https://www.twitter.com/"}'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Invalid social media link", "success": false}}')

    def test_update_invalid_url_start(self):
        self.request.POST = {'project': '59', 'data': '{"field": "twitter", "value": "witter.com/"}'}

        response = update_project(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Invalid social media link", "success": false}}')


class UpdatePostTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def setUp(self):
        # todo this ideally should be mocked by patching project_ajax_request
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.project = Project.objects.get(id=59)
        ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

        self.factory = RequestFactory()
        self.request = self.factory.post('/test/', content_type='application/json')
        self.request._dont_enforce_csrf_checks = True
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.request.POST = self.request.POST.copy()
        self.request.user = self.user

    def test_data_not_in_post(self):
        self.request.POST = {'project': '59'}

        response = update_post(self.request)
        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "No data in request", "success": false}}')

    def test_field_not_in_post(self):
        self.request.POST = {'project': '59', 'data': '{"somethign": "nothing"}'}

        response = update_post(self.request)
        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_post_not_in_post(self):
        self.request.POST = {'project': '59', 'data': '{"field": "nothing"}'}

        response = update_post(self.request)
        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_body_not_in_post(self):
        self.request.POST = {'project': '59', 'data': '{"field": "post"}'}

        response = update_post(self.request)
        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_update_post(self):
        self.request.POST = {'project': '59', 'data': '{"field": "post", "post": 46}', 'body': 'post test'}

        response = update_post(self.request)
        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        post = Post.objects.get(id=46)
        self.assertEqual(post.post, 'post test')

    def test_update_title(self):
        self.request.POST = {'project': '59', 'data': '{"field": "title", "post": 46}', 'body': 'title test'}

        response = update_post(self.request)
        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        post = Post.objects.get(id=46)
        self.assertEqual(post.title, 'title test')

    def test_update_published(self):
        post = Post.objects.get(id=46)
        self.assertEqual(post.is_published, True)

        self.request.POST = {'project': '59', 'data': '{"field": "published", "value": false, "post": 46}'}

        response = update_post(self.request)
        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        post = Post.objects.get(id=46)
        self.assertEqual(post.is_published, False)

    def test_update_author(self):
        post = Post.objects.get(id=46)
        self.assertEqual(post.is_published, True)

        self.request.POST = {'project': '59', 'data': '{"field": "author", "value": "'+ self.user.username +'", "post": 46}'}

        response = update_post(self.request)
        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        post = Post.objects.get(id=46)
        self.assertEqual(post.author, self.user)

class ImageUploadTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def setUp(self):
        # todo this ideally should be mocked by patching project_ajax_request
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.project = Project.objects.get(id=59)
        ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

        self.factory = RequestFactory()
        self.request = self.factory.post('/test/', content_type='application/json')
        self.request._dont_enforce_csrf_checks = True
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.request.POST = self.request.POST.copy()
        self.request.user = self.user

    def test_no_file_in_request(self):
        self.request.POST = {'project': '59', 'logo': 'true'}

        response = image_upload(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "No image in request", "success": false}}')

    @patch('projects.models.Project.logo')
    def test_upload_logo(self, mock_project_logo):
        self.request.POST = {'project': '59', 'logo': 'true'}
        file = SimpleUploadedFile("file.txt", "file_content")
        self.request.FILES['file'] = file

        response = image_upload(self.request)

        self.response_200(response=response)

# todo complete image upload delete


class AddCreatorTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def setUp(self):
        # todo this ideally should be mocked by patching project_ajax_request
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.project = Project.objects.get(id=59)
        ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

        self.factory = RequestFactory()
        self.request = self.factory.post('/test/', content_type='application/json')
        self.request._dont_enforce_csrf_checks = True
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.request.POST = self.request.POST.copy()
        self.request.user = self.user

    def test_no_username_in_request(self):
        self.request.POST = {'project': '59', 'logo': 'true'}

        response = add_creator(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "No username in request", "success": false}}')

    def test_user_already_assigned_to_project(self):
        self.request.POST = {'project': '59', 'logo': 'true', 'username': self.user.username}

        response = add_creator(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "User already assigned to project", "success": false}}')

    def test_valid_request(self):
        new_creator = User.objects.create_user('new_creator', 'new_creator@somewhere.com', 'password')
        self.request.POST = {'project': '59', 'logo': 'true', 'username': new_creator.username}

        response = add_creator(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')


class RemoveCreatorTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def setUp(self):
        # todo this ideally should be mocked by patching project_ajax_request
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.project = Project.objects.get(id=59)
        self.creator = ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

        self.factory = RequestFactory()
        self.request = self.factory.post('/test/', content_type='application/json')
        self.request._dont_enforce_csrf_checks = True
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.request.POST = self.request.POST.copy()
        self.request.user = self.user

    def test_no_username_in_request(self):
        self.request.POST = {'project': '59', 'logo': 'true'}

        response = remove_creator(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "No username in request", "success": false}}')

    def test_user_not_assigned_to_project(self):
        self.creator.delete()
        self.request.POST = {'project': '59', 'logo': 'true', 'username': self.user.username}

        response = remove_creator(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Object does not exist", "success": false}}')

    def test_valid_request(self):
        self.request.POST = {'project': '59', 'logo': 'true', 'username': self.user.username}

        response = remove_creator(self.request)

        creator = ProjectCreator.objects.get(project=self.project, creator=self.user)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')
        self.assertEqual(creator.is_active, False)


class UpdateCreatorTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def setUp(self):
        # todo this ideally should be mocked by patching project_ajax_request
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.project = Project.objects.get(id=59)
        self.creator = ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

        self.factory = RequestFactory()
        self.request = self.factory.post('/test/', content_type='application/json')
        self.request._dont_enforce_csrf_checks = True
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.request.POST = self.request.POST.copy()
        self.request.user = self.user

    def test_no_username_in_request(self):
        self.request.POST = {'project': '59', 'logo': 'true'}

        response = update_creator(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_user_not_assigned_to_project(self):
        self.creator.delete()
        self.request.POST = {'project': '59', 'logo': 'true', 'username': self.user.username}

        response = remove_creator(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Object does not exist", "success": false}}')

    def test_field_missing_in_request(self):
        self.request.POST = {'project': '59', 'username': self.user.username}

        response = update_creator(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_body_missing_from_request(self):
        self.request.POST = {'project': '59', 'field': 'summary', 'username': self.user.username}

        response = update_creator(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_value_missing_from_request(self):
        self.request.POST = {'project': '59', 'field': 'admin', 'username': self.user.username}

        response = update_creator(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_valid_summary_update(self):
        self.request.POST = {'project': '59', 'field': 'summary', 'username': self.user.username, 'body': 'new summary'}

        response = update_creator(self.request)

        creator = ProjectCreator.objects.get(project=self.project, creator=self.user)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')
        self.assertEqual(creator.summary, 'new summary')

    def test_valid_admin_update(self):
        self.request.POST = {'project': '59', 'field': 'admin', 'value': 'false', 'username': self.user.username}

        response = update_creator(self.request)

        creator = ProjectCreator.objects.get(project=self.project, creator=self.user)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')
        self.assertEqual(creator.is_admin, False)


class AddTechnologyTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def setUp(self):
        # todo this ideally should be mocked by patching project_ajax_request
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.project = Project.objects.get(id=59)
        self.creator = ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

        self.factory = RequestFactory()
        self.request = self.factory.post('/test/', content_type='application/json')
        self.request._dont_enforce_csrf_checks = True
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.request.POST = self.request.POST.copy()
        self.request.user = self.user

    def test_technology_missing_from_request(self):
        self.request.POST = {'project': '59'}

        response = add_technology(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_add_valid_technology(self):
        self.request.POST = {'project': '59', 'technology': 'new_technology'}

        response = add_technology(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        technology = Technologies.objects.get(name='New_Technology')
        project_technology = ProjectTechnologies.objects.get(technology=technology, project=self.project)


class RemoveTechnologyTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def setUp(self):
        # todo this ideally should be mocked by patching project_ajax_request
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.project = Project.objects.get(id=59)
        self.creator = ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

        self.factory = RequestFactory()
        self.request = self.factory.post('/test/', content_type='application/json')
        self.request._dont_enforce_csrf_checks = True
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.request.POST = self.request.POST.copy()
        self.request.user = self.user

    def test_technology_missing_from_request(self):
        self.request.POST = {'project': '59'}

        response = remove_technology(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_delete_valid_technology(self):
        technology = Technologies.objects.create(name='new_technology')
        project_technology = ProjectTechnologies.objects.create(technology=technology, project=self.project)
        start_technology_count = self.project.technologies.count()

        self.request.POST = {'project': '59', 'technology': technology.name}

        response = remove_technology(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        end_technology_count = self.project.technologies.count()
        self.assertEqual(start_technology_count, end_technology_count + 1)


class UpdateTechnologyTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def setUp(self):
        # todo this ideally should be mocked by patching project_ajax_request
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.project = Project.objects.get(id=59)
        self.creator = ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

        self.factory = RequestFactory()
        self.request = self.factory.post('/test/', content_type='application/json')
        self.request._dont_enforce_csrf_checks = True
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.request.POST = self.request.POST.copy()
        self.request.user = self.user

    def test_technology_missing_from_request(self):
        self.request.POST = {'project': '59', 'strength': '22'}

        response = update_technology(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_strength_missing_from_request(self):
        self.request.POST = {'project': '59', 'technology': 'something'}

        response = update_technology(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_update_valid_technology(self):
        technology_name = 'New Technology'
        self.request.POST = {'project': '59', 'technology': technology_name, 'strength': '22'}

        technology = Technologies.objects.create(name=technology_name)
        project_technology = ProjectTechnologies.objects.create(technology=technology, project=self.project, strength=100)
        start_technology_count = self.project.technologies.count()

        response = update_technology(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        end_technology_count = self.project.technologies.count()
        self.assertEqual(start_technology_count, end_technology_count)
        project_technology = ProjectTechnologies.objects.get(technology=technology, project=self.project)
        self.assertEqual(project_technology.strength, 22)



class AddTagTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def setUp(self):
        # todo this ideally should be mocked by patching project_ajax_request
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.project = Project.objects.get(id=59)
        self.creator = ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

        self.factory = RequestFactory()
        self.request = self.factory.post('/test/', content_type='application/json')
        self.request._dont_enforce_csrf_checks = True
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.request.POST = self.request.POST.copy()
        self.request.user = self.user

    def test_technology_missing_from_request(self):
        self.request.POST = {'project': '59'}

        response = add_tag(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_add_valid_text(self):
        self.request.POST = {'project': '59', 'tag': 'new_tag'}
        tags = self.project.tags.names()
        self.assertEqual(len(tags), 0)

        response = add_tag(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        tags = self.project.tags.names()
        self.assertTrue(len(tags), 1)
        self.assertTrue(u'new_tag' in tags)

class RemoveTagTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def setUp(self):
        # todo this ideally should be mocked by patching project_ajax_request
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.project = Project.objects.get(id=59)
        self.creator = ProjectCreator.objects.create(project=self.project, creator=self.user, is_admin=True)

        self.factory = RequestFactory()
        self.request = self.factory.post('/test/', content_type='application/json')
        self.request._dont_enforce_csrf_checks = True
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.request.POST = self.request.POST.copy()
        self.request.user = self.user

    def test_technology_missing_from_request(self):
        self.request.POST = {'project': '59'}

        response = remove_tag(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Required data missing from request", "success": false}}')

    def test_delete_valid_technology(self):
        tag_name = u'new_tag'
        self.request.POST = {'project': '59', 'tag': tag_name}

        self.project.tags.add(tag_name)
        self.assertEqual(len(self.project.tags.names()), 1)
        self.assertEqual(self.project.tags.names()[0], tag_name)

        response = remove_tag(self.request)

        self.response_200(response=response)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"success": true}}')

        self.assertEqual(len(self.project.tags.names()), 0)

@project_ajax_request
def mock_function(request, project, *args, **kwargs):
    return "successful response"

class ProjectAjaxRequestTestCase(TestCase):
    fixtures = ['initial_project_data.json', 'initial_user_data.json']

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user('someone', 'someone@somewhere.com', 'password')
        self.client.login(username='someone', password='password')

        self.factory = RequestFactory()

    def test_missing_csrf_token(self):
        request = self.factory.post('/test/')
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        response = mock_function(request)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['status'], 403)
        self.assertEqual(content['statusText'], 'FORBIDDEN')

    def test_invalid_put_request(self):
        request = self.factory.put('/test/')
        request._dont_enforce_csrf_checks = True
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = mock_function(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": null}')

    def test_project_not_in_request(self):
        request = self.factory.post('/test/')
        request._dont_enforce_csrf_checks = True
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = mock_function(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": null}')

    def test_user_not_creator(self):
        request = self.factory.post('/test/', content_type='application/json')
        request._dont_enforce_csrf_checks = True
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        request.POST = request.POST.copy()
        request.POST = {'project': '59'}
        request.user = AnonymousUser()
        response = mock_function(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Object does not exist", "success": false}}')

    def test_user_not_admin(self):
        project = Project.objects.get(id=59)
        ProjectCreator.objects.create(project=project, creator=self.user, is_admin=False)

        request = self.factory.post('/test/', content_type='application/json')
        request._dont_enforce_csrf_checks = True
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        request.POST = request.POST.copy()
        request.POST = {'project': '59'}

        request.user = self.user

        response = mock_function(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": {"message": "Only admins can make an update to a project", "success": false}}')

    def test_successful_request(self):
        project = Project.objects.get(id=59)
        ProjectCreator.objects.create(project=project, creator=self.user, is_admin=True)

        request = self.factory.post('/test/', content_type='application/json')
        request._dont_enforce_csrf_checks = True
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        request.POST = request.POST.copy()
        request.POST = {'project': '59'}

        request.user = self.user

        response = mock_function(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"status": 200, "statusText": "OK", "content": "successful response"}')
