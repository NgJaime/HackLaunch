from django.shortcuts import redirect
from social.exceptions import InvalidEmail
from social.pipeline.partial import partial
from models import UserProfile

def user_password(strategy, user, is_new=False, *args, **kwargs):
    if 'backend' not in kwargs or kwargs['backend'].name != 'email':
        return

    password = kwargs['response']['password']
    if not user.nonSocialAuth:
        user.nonSocialAuth = True
        user.set_password(password)
        user.save()

    elif not user.check_password(password):
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
            kwargs['requested_email'] = True
            return redirect('require_email')


def load_extra_data(backend, details, response, uid, user, *args, **kwargs):
    social = kwargs.get('social') or \
             backend.strategy.storage.user.get_social_auth(backend.name, uid)
    if social:
        extra_data = backend.extra_data(user, uid, response, details)
        set_extra_data(user, extra_data)


def set_extra_data(user, extra_data=None):
    if user is not None and extra_data:
        try:
            profile = UserProfile.objects.get(user_id=user.id)
        except UserProfile.DoesNotExist:
            profile = None

        if 'location' in extra_data:
            if profile is not None and profile.location is None:
                # todo need to update for logins other than linkedin
                profile.location = extra_data['location']['name']
                profile.save()
            elif profile is None:
                profile, created = UserProfile.objects.update_or_create(user_id=user.id, location=extra_data['location']['name'])
                profile.save()

        if profile is not None \
                and user.minimalProfile is False \
                and profile.location is not None \
                and user.first_name is not None \
                and user.last_name is not None:
                    user.minimalProfile = True
                    user.save()


@partial
def mail_validation(backend, details, is_new=False, *args, **kwargs):
    if (is_new and 'email' in kwargs['request']) \
        or 'requested_email' in kwargs:
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

