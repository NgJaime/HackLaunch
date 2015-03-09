from django.shortcuts import redirect
from social.exceptions import AuthException
from social.pipeline.partial import partial

def user_password(strategy, user, is_new=False, *args, **kwargs):
    if 'backend' not in kwargs or \
                    kwargs['backend'].name != 'email':
        return

    password = kwargs['response']['password']
    if is_new:
        user.set_password(password)
        user.save()

    elif not user.check_password(password):
        return {'user': None, 'social': None}
        # raise AuthException(strategy.backend)


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and user.email:
        return
    elif is_new and not details.get('email'):
        if strategy.session_get('saved_email'):
            details['email'] = strategy.session_pop('saved_email')
        else:
            return redirect('require_email')
