from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files import File
from django.template import RequestContext
from django.http import Http404
from mock import MagicMock, patch
from social.apps.django_app.default.models import UserSocialAuth

from users.models import User, UserProfile, Skill

from users.views import ProfileEditView, profile_view, require_email, validation_sent, delete_user, logout


def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


def add_middleware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


class ProfileEditViewTestCase(TestCase):
    fixtures = ['maker_types.json', 'skills.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user('bob', first_name='bob', last_name='doe', email='bob@abc.com')
        self.profile1 = UserProfile.objects.create(user=self.user1, location='over there',
                                                   summary='something')

    # def tearDown(self):
        # self.user1.delete()
        # self.profile1.delete()

    def test_form_valid_anonymous_user(self):
        request = self.factory.post('/profile/')
        request.user = AnonymousUser()

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        response = ProfileEditView.as_view()(request)

        self.assertEqual(response.url, '/login?next=/profile/')

    def test_initial_data_profile_exists(self):
        request = self.factory.post('/profile/')
        request.user = self.user1

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        profile_edit_view = ProfileEditView()
        profile_edit_view.request = request
        initial = profile_edit_view.get_initial()

        self.assertEqual('bob@abc.com', initial['email'])
        self.assertEqual('bob', initial['first_name'])
        self.assertEqual('doe', initial['last_name'])
        self.assertEqual('over there', initial['location'])
        self.assertEqual([], initial['maker_type'])
        self.assertEqual([], initial['skills'])
        self.assertEqual('something', initial['summary'])

    def test_form_valid_no_changes(self):
        form = MagicMock()
        form.profile.save.return_value = True
        form.profile.user.save.return_value = True
        form.changed_data = []

        profile_edit_view = ProfileEditView()
        response = profile_edit_view.form_valid(form)

        self.assertEqual(response.url, '/')
        self.assertEqual(form.profile.save.call_count, 0)
        self.assertEqual(form.profile.user.save.call_count, 0)

    def test_form_valid_skills_changed(self):

        form = MagicMock()
        form.cleaned_data = {'skills': [8, 17, 18]}
        form.changed_data = ['skills']

        profile_edit_view = ProfileEditView()
        profile_edit_view.profile = self.profile1
        response = profile_edit_view.form_valid(form)

        profile_skills = self.profile1.skills.all()

        self.assertEqual(response.url, '/')
        self.assertEqual(len(profile_skills), 3)
        self.assertEqual(profile_skills[0].pk, 8)
        self.assertEqual(profile_skills[1].pk, 17)
        self.assertEqual(profile_skills[2].pk, 18)

    @patch('users.models.UserProfile.save')
    def test_form_valid_picture_changed_existing_image(self, mock_user_profile_save):
        mock_user_profile_save = MagicMock()

        old_image_thumb_mock = MagicMock()
        old_image_thumb_mock.name = 'old_mock_image_thumb'
        old_image_thumb_mock.delete.return_value = True

        old_image_mock = MagicMock(spec=File, name='FileMock')
        old_image_mock.name = 'old_mock_image'

        self.profile1.image = old_image_mock;
        self.profile1.thumbnail = old_image_thumb_mock;

        # just to be sure
        self.assertEqual(self.profile1.image, old_image_mock)
        self.assertEqual(self.profile1.thumbnail, old_image_thumb_mock)

        new_image_mock = MagicMock(spec=File, name='FileMock')
        new_image_mock.name = 'new_mock_image'

        delete_mock = MagicMock()
        delete_mock.delete.return_value = True

        form = MagicMock()
        form.cleaned_data = {'image': new_image_mock}
        form.changed_data = ['image']
        form.initial = {'image': delete_mock}

        profile_edit_view = ProfileEditView()
        profile_edit_view.profile = self.profile1
        response = profile_edit_view.form_valid(form)

        # todo not checking delete of thumb
        self.assertEqual(response.url, '/')
        self.assertEqual(delete_mock.delete.call_count, 1)
        self.assertEqual(self.profile1.image, new_image_mock)
        self.assertEqual(self.profile1.thumbnail, new_image_mock)

    @patch('django.db.models.fields.files.ImageFieldFile')
    @patch('users.models.UserProfile.save')
    def test_form_valid_picture_changed_no_existing_image(self, mock_user_profile_save, mock_ImageFieldFile):
        mock_user_profile_save = MagicMock()
        mock_ImageFieldFile = MagicMock()

        new_image_mock = MagicMock(spec=File, name='FileMock')
        new_image_mock.name = 'new_mock_image'

        delete_mock = MagicMock()
        delete_mock.delete.return_value = True

        form = MagicMock()
        form.cleaned_data = {'image': new_image_mock}
        form.changed_data = ['image']
        form.initial = {}

        profile_edit_view = ProfileEditView()
        profile_edit_view.profile = self.profile1
        response = profile_edit_view.form_valid(form)

        self.assertEqual(response.url, '/')
        self.assertEqual(self.profile1.image, new_image_mock)
        self.assertEqual(self.profile1.thumbnail, new_image_mock)

    def test_form_valid_password_changed(self):
        form = MagicMock()
        form.cleaned_data = {'password': 'abc123'}
        form.changed_data = ['password']

        self.profile1.user.set_password = MagicMock()
        self.profile1.user.save = MagicMock()

        profile_edit_view = ProfileEditView()
        profile_edit_view.profile = self.profile1
        response = profile_edit_view.form_valid(form)

        self.assertEqual(response.url, '/password_changed_login')
        self.assertEqual( self.profile1.user.save.call_count, 1)
        self.assertEqual(self.profile1.user.set_password.call_count, 1)

    def test_form_valid_profile_changed(self):
        form = MagicMock()
        form.cleaned_data = {'summary': 'something new'}
        form.changed_data = ['summary']

        profile_edit_view = ProfileEditView()
        profile_edit_view.profile = self.profile1
        response = profile_edit_view.form_valid(form)

        self.assertEqual(response.url, '/')
        self.assertEqual( self.profile1.summary, 'something new')

    def test_form_valid_profile_user_changed(self):
        form = MagicMock()
        form.cleaned_data = {'first_name': 'new name'}
        form.changed_data = ['first_name']

        profile_edit_view = ProfileEditView()
        profile_edit_view.profile = self.profile1
        response = profile_edit_view.form_valid(form)

        self.assertEqual(response.url, '/')
        self.assertEqual( self.profile1.user.first_name, 'new name')

    def test_form_invalid_pop_invalid_password_error(self):
        form = MagicMock()
        form.errors = {'password': [u'This field is required.'], 'password_confirmation': [u'This field is required.']}

        request = self.factory.post('/profile/')
        request.user = self.user1
        self.user1.nonSocialAuth = False

        profile_edit_view = ProfileEditView()
        profile_edit_view.request = request
        response = profile_edit_view.form_invalid(form)

        self.assertEqual(response.url, '/')
        self.assertEqual(len(form.errors), 0)

    def test_form_invalid_pop_valid_password_error(self):
        form = MagicMock()
        form.errors = {'password': [u'This field is required.'], 'password_confirmation': [u'This field is required.']}

        request = self.factory.post('/profile/')
        request.user = self.user1
        self.user1.nonSocialAuth = True

        profile_edit_view = ProfileEditView()
        profile_edit_view.request = request
        response = profile_edit_view.form_invalid(form)

        self.assertEqual(response.template_name[0], 'profile_edit.html')
        self.assertEqual(len(response.context_data['form'].errors), 2)
        self.assertEqual(response.context_data['form'].errors['password'], [u'This field is required.'])
        self.assertEqual(response.context_data['form'].errors['password_confirmation'], [u'This field is required.'])

    def test_form_invalid(self):
        form = MagicMock()
        form.errors = {'first_name': [u'I dont like your name.']}

        request = self.factory.post('/profile/')
        request.user = self.user1
        self.user1.nonSocialAuth = False

        profile_edit_view = ProfileEditView()
        profile_edit_view.request = request
        response = profile_edit_view.form_invalid(form)

        self.assertEqual(response.template_name[0], 'profile_edit.html')
        self.assertEqual(len(response.context_data['form'].errors), 1)
        self.assertEqual(response.context_data['form'].errors['first_name'], [u'I dont like your name.'])


class ProfileViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user('bob', first_name='bob', last_name='doe', email='bob@abc.com')
        self.profile1 = UserProfile.objects.create(user=self.user1, location='over there',
                                                   summary='something nice')

    def test_valid_slug(self):
        request = self.factory.get('profile')
        request.user = self.user1

        response = profile_view(request, slug='bob')

        # todo this is a little fragile assert something more useful
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('<p>something nice</p>', response.content)
        self.assertInHTML('<h1><strong>bob doe</strong></h1>', response.content)
        self.assertInHTML('<td>over there</td>', response.content)

    def test_invalid_slug(self):
        request = self.factory.get('profile')
        request.user = self.user1

        try:
            response = profile_view(request, slug='not_bob')
        except Http404:
            pass
        else:
            self.assertFalse()


class RequireEmailTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_post_with_email(self):
        request = self.factory.post('require_email', {'email': 'abc@123.com'})
        request.session = {'partial_pipeline': {'backend': 'email'}}

        response = require_email(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/complete/email')
        self.assertEqual(request.session['saved_email'], 'abc@123.com')

    @patch('users.views.render_to_response')
    def test_post_no_email(self, mock_render_to_response):
        request = self.factory.post('require_email')
        request.session = {'partial_pipeline': {'backend': 'email'}}

        response = require_email(request)

        mock_render_to_response.assert_called_once_with('require_email.html', RequestContext(request))

    @patch('users.views.render_to_response')
    def test_get(self, mock_render_to_response):
        request = self.factory.get('require_email')

        require_email(request)

        mock_render_to_response.assert_called_once_with('require_email.html', RequestContext(request))


class ValidationSentTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('users.views.render')
    def test_email_in_session(self, mock_render):
        request = self.factory.get('validation_sent')
        request.session = {'email_validation_address': 'abc@123.com'}

        validation_sent(request)

        mock_render.assert_called_once_with(request, 'validation_sent.html', {'email': request.session['email_validation_address']})


class DeleteUserTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('bob', first_name='bob', last_name='doe', email='bob@abc.com')
        self.user_no_profile = User.objects.create_user('jim')
        self.profile = UserProfile.objects.create(user=self.user, location='over there', summary='something')
        self.socialAuth = UserSocialAuth.objects.create(user=self.user)

    @patch('users.views.login_required', MagicMock)
    def test_user_to_delete(self):
        request = RequestFactory()
        request.user = self.user

        response = delete_user(request)

        self.assertEqual(response.url, '/logout')
        self.assertEqual(response.status_code, 302)

    @patch('users.views.login_required', MagicMock)
    def test_no_user_to_delete(self):
        request = RequestFactory()
        request.user = self.user_no_profile

        try:
            delete_user(request)
        except Http404:
            pass
        else:
            self.assertFalse()

class LogoutTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch('users.views.auth_logout')
    def test_logout(self, mock_auth_logout):
        request = self.factory.request()

        mock_auth_logout = MagicMock()
        mock_auth_logout(request).return_value = None

        response = logout(request)

        self.assertEqual(response.url, '/')
        self.assertEqual(response.status_code, 302)
        mock_auth_logout.assert_called_once_with(request)






