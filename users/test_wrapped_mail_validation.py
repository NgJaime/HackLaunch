from django.test import SimpleTestCase
from mock import MagicMock, patch

import social.pipeline.partial
import imp


@patch('social.pipeline.mail.mail_validation')
class WrappedMailValidationTestCase(SimpleTestCase):

    @patch('users.pipeline.partial')
    def test_new_user_email_in_request(self, mock_mail_validation, mock_partial):
        mail_validation = MagicMock()
        mock_partial = MagicMock()

        imp.reload(social.pipeline.partial)

        from users.pipeline import wrapped_mail_validation

        args = (None, None)
        kwargs = {
            'request': {'email': 'someone@somewhere.com'},
            'is_new': True,
            'details': {},
            'backend': None
        }

        wrapped_mail_validation(*args, **kwargs)

        self.assertEqual(mock_mail_validation.call_count, 1)


    def test_verification_in_request(self, mock_mail_validation):
        mail_validation = MagicMock

        imp.reload(social.pipeline.partial)

        from users.pipeline import wrapped_mail_validation

        args = (None, None)
        kwargs = {
            'request': {'verification_code': 'abc'},
            'is_new': True,
            'details': {},
            'backend': None
        }

        wrapped_mail_validation(*args, **kwargs)

        self.assertEqual(mock_mail_validation.call_count, 1)


    @patch('social.pipeline.mail.mail_validation')
    def test_no_email_no_verification_code(self, mock_mail_validation):
        args = (None, None)
        kwargs = {
            'request': {},
            'is_new': True,
            'details': {},
            'backend': None
        }

        from users.pipeline import wrapped_mail_validation
        wrapped_mail_validation(*args, **kwargs)

        self.assertEqual(mock_mail_validation.call_count, 0)
