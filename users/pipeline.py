from django.shortcuts import redirect
from social.pipeline.partial import partial
from social.pipeline.mail import mail_validation
from social.exceptions import InvalidEmail
from models import UserProfile


def user_password(strategy, user, is_new=False, *args, **kwargs):
    if 'backend' not in kwargs or kwargs['backend'].name != 'email':
        return

    if 'response' in kwargs and 'password' in kwargs['response']:
        password = kwargs['response']['password']
        if not user.nonSocialAuth:
            user.nonSocialAuth = True
            user.set_password(password)
            user.save()
            return
        elif user.check_password(password):
            return

    return {'user': None, 'social': None}

@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and user.email:
        return
    elif is_new and 'email' in kwargs['request']:
        details['email'] = kwargs['request']['email']
    elif is_new and not details.get('email'):
        if strategy.session_get('saved_email'):
            details['email'] = strategy.session_pop('saved_email')
        else:
            return redirect('require_email')


def load_extra_data(backend, details, response, uid, user, *args, **kwargs):
    social = kwargs.get('social') or \
             backend.strategy.storage.user.get_social_auth(backend.name, uid)
    if social:
        extra_data = backend.extra_data(user, uid, response, details)
        set_extra_data(user, extra_data)


def set_extra_data(user, extra_data=None):
    if user is not None:
        profile, created = UserProfile.objects.get_or_create(user_id=user.id)

        if extra_data and 'location' in extra_data:
            if profile.location is None:
                # todo need to update for logins other than linked-in
                profile.location = extra_data['location']['name']
                profile.save()

@partial
def wrapped_mail_validation(backend, details, is_new=False, *args, **kwargs):
    if (is_new and 'email' in kwargs['request']) \
            or 'verification_code' in kwargs['request']:

        requires_validation = backend.REQUIRES_EMAIL_VALIDATION or \
                          backend.setting('FORCE_EMAIL_VALIDATION', False)
        send_validation = details.get('email') and \
                          (is_new or backend.setting('PASSWORDLESS', False))
        if requires_validation and send_validation:
            data = backend.strategy.request_data()
            if 'verification_code' in data:
                backend.strategy.session_pop('email_validation_address')
                if not backend.strategy.validate_email(details['email'],
                                               data['verification_code']):
                    raise InvalidEmail(backend)
            else:
                backend.strategy.send_email_validation(backend, details['email'])
                backend.strategy.session_set('email_validation_address',
                                             details['email'])
                return backend.strategy.redirect(
                    backend.strategy.setting('EMAIL_VALIDATION_URL')
                )
