from django.shortcuts import redirect
from social.pipeline.partial import partial
from models import UserProfile

def user_password(strategy, user, is_new=False, *args, **kwargs):
    if 'backend' not in kwargs or \
                    kwargs['backend'].name != 'email':
        return

    password = kwargs['response']['password']
    if is_new:
        user.nonSocialAuth = True
        user.set_password(password)
        user.save()

    elif not user.check_password(password):
        return {'user': None, 'social': None}


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and user.email:
        return
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
    if extra_data:
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
                profile, created = UserProfile.objects.update_or_create({'user_id': user.id, 'location': extra_data['location']['name']})
                profile.save()

        if user.minimalProfile is False and profile.location is not None \
                and user.first_name is not None and user.last_name is not None:
                    user.minimalProfile = True
                    user.save()

