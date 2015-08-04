from django.test import SimpleTestCase, TestCase
from django.http.response import HttpResponseRedirect
from mock import MagicMock, Mock, patch
from users.pipeline import user_password, require_email, set_extra_data, load_extra_data
from users.models import UserProfile, User


class UserPasswordTestCase(SimpleTestCase):

    def test_backend_Not_Email(self):
        backend = Mock()
        backend.name = 'something_else'

        result = user_password(None, None, backend=backend)

        self.assertIsNone(result)

    def test_no_backend(self):
        result = user_password(None, None)

        self.assertIsNone(result)

    def test_no_response(self):
        backend = Mock()
        backend.name = 'email'

        result = user_password(None, None, backend=backend)

        self.assertDictEqual(result, {'user': None, 'social': None}, msg="Missing response invalid result")

    def test_no_password_in_response(self):
        backend = Mock()
        backend.name = 'email'

        result = user_password(None, None, backend=backend, response={})

        self.assertDictEqual(result, {'user': None, 'social': None}, msg="Missing response invalid result")

    def test_password_correct_nonSocialAuth_true(self):
        backend = Mock()
        backend.name = 'email'
        user = MagicMock()
        user.nonSocialAuth = True
        user.check_password.return_value = True

        result = user_password(None, user, backend=backend, response={'password': 'something'})

        self.assertIsNone(result)
        self.assertEqual(user.check_password.call_count, 1)

    def test_password_incorrect_nonSocialAuth_true(self):
        backend = Mock()
        backend.name = 'email'
        user = MagicMock()
        user.nonSocialAuth = True
        user.check_password.return_value = False

        result = user_password(None, user, backend=backend, response={'password': 'something'})

        self.assertDictEqual(result, {'user': None, 'social': None}, msg="Missing response invalid result")
        self.assertEqual(user.check_password.call_count, 1)

    def test_password_correct_nonSocialAuth_false(self):
        backend = Mock()
        backend.name = 'email'
        user = MagicMock()
        user.nonSocialAuth = False
        user.check_password.return_value = True

        result = user_password(None, user, backend=backend, response={'password': 'something'})

        self.assertIsNone(result)
        self.assertEqual(user.set_password.call_count, 1)
        self.assertEqual(len(user.set_password.call_args[0]), 1)
        self.assertEqual(user.set_password.call_args[0][0], 'something')
        self.assertEqual(user.save.call_count, 1)
        self.assertEqual(user.nonSocialAuth, True)


class UserRequireEmailTestCase(SimpleTestCase):

    def test_user_has_email(self):
        user = MagicMock()
        user.email = True

        args = (None, None)
        kwargs = {
            'user': user,
            'details': {},
        }

        result = require_email(*args, **kwargs)

        self.assertDictEqual(result, {})

    def test_new_user_new_email(self):
        user = MagicMock()
        user.email = False

        args = (None, None)
        kwargs = {
            'user': user,
            'details': {},
            'is_new': True,
            'request': {'email': 'a@b.com'}
        }

        result = require_email(*args, **kwargs)

        self.assertDictEqual(result, {})
        self.assertEqual(kwargs['details']['email'], 'a@b.com')

    def test_new_user_no_email_request_email_in_session(self):
        user = MagicMock()
        user.email = False
        strategy = MagicMock()
        strategy.session_get('saved_email').return_value = True
        strategy.session_pop('saved_email').return_value = 'a@b.com'

        args = (strategy, None)
        kwargs = {
            'user': user,
            'details': {},
            'is_new': True,
            'request': {'email': 'a@b.com'}
        }

        result = require_email(*args, **kwargs)

        self.assertTrue('email' in kwargs['details'])
        self.assertEqual(strategy.session_pop('saved_email').return_value, kwargs['details']['email'])
        self.assertDictEqual(result, {})

    def test_new_user_no_email(self):
        user = MagicMock()
        user.email = False
        strategy = MagicMock()
        strategy.session_get.return_value = False
        strategy.session_get('saved_email')

        args = (strategy, None)
        kwargs = {
            'user': user,
            'details': {},
            'is_new': True,
            'request': {}
        }

        result = require_email(*args, **kwargs)

        self.assertTrue(result, HttpResponseRedirect)
        self.assertEqual(result.url, '/email_required/')


class SetExtraDataTestCase(TestCase):

    def setUp(self):
        self.user_with_profile_and_location = User.objects.create_user('bob')
        self.user_with_profile_no_location = User.objects.create_user('jon')
        self.user_no_profile = User.objects.create_user('sandy')
        self.profile1 = UserProfile.objects.create(user=self.user_with_profile_and_location, location='over there')
        self.profile2 = UserProfile.objects.create(user=self.user_with_profile_no_location)

    def tearDown(self):
        self.user_with_profile_and_location.delete()
        self.user_no_profile.delete()
        self.profile1.delete()

    def test_user_none(self):
        result = set_extra_data(None)

        self.assertIsNone(result)
        self.assertEqual(UserProfile.objects.count(), 2)

    def test_extra_data_none(self):

        result = set_extra_data(self.user_with_profile_and_location)

        self.assertIsNone(result)
        self.assertEqual(UserProfile.objects.count(), 2)

    def test_no_profile_no_location_extra_data(self):
        result = set_extra_data(self.user_no_profile, {'something': None})

        self.assertIsNone(result)
        self.assertEqual(UserProfile.objects.count(), 3)

    def test_no_profile_location_available(self):
        extra_data = {'location': {'name': 'somewhere'}}

        result = set_extra_data(self.user_no_profile, extra_data=extra_data)

        new_profile = UserProfile.objects.filter(user_id=self.user_no_profile.id)

        self.assertIsNone(result)
        self.assertEqual(UserProfile.objects.count(), 3)
        self.assertTrue(len(new_profile), 1)
        self.assertTrue(new_profile[0].location, u'somewhere')

        new_profile[0].delete()

    def test_no_location_in_profile_available_extra_data(self):
        extra_data = {'location': {'name': 'somewhere'}}

        result = set_extra_data(self.user_with_profile_no_location, extra_data=extra_data)

        new_profile = UserProfile.objects.filter(user_id=self.user_with_profile_no_location.id)

        self.assertIsNone(result)
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertTrue(len(new_profile), 1)
        self.assertTrue(new_profile[0].location, u'somewhere')

    def test_location_in_profile_available_extra_data(self):
        extra_data = {'location': {'name': 'somewhere'}}

        result = set_extra_data(self.user_with_profile_and_location, extra_data=extra_data)

        new_profile = UserProfile.objects.filter(user_id=self.user_with_profile_and_location.id)

        self.assertIsNone(result)
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertTrue(len(new_profile), 1)
        self.assertTrue(new_profile[0].location, u'over there')

@patch('users.pipeline.set_extra_data')
class LoadExtraDataTestCase(TestCase):

    def test_not_social_account(self, mock_set_extra_data):
        backend = MagicMock()
        backend.strategy.storage.user.get_social_auth.return_value = False

        load_extra_data(backend, None, None, None, None, None, {})

        self.assertEqual(mock_set_extra_data.call_count, 0)

    def test_social_account(self, mock_set_extra_data):
        backend = MagicMock()
        backend.strategy.storage.user.get_social_auth.return_value = False

        kwargs = { 'social': True }

        load_extra_data(backend, None, None, None, None, None, **kwargs)

        self.assertEqual(mock_set_extra_data.call_count, 1)
