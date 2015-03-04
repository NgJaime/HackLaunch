from social.exceptions import AuthException


def user_password(strategy, user, is_new=False, *args, **kwargs):
    if  'backend' not in kwargs or \
                    kwargs['backend'].name != 'email':
        return

    password = strategy.request_data()['password']
    if is_new:
        user.set_password(password)
        user.save()

        # fields = {'email': strategy.request_data()['email']}
        #
        # user = strategy.create_user(fields)
        # user.set_password(password)
        # user.save()
        #
        # return {
        #     'is_new': True,
        #     'user': user
        # }

    elif not user.validate_password(password):
        # return {'user': None, 'social': None}
        raise AuthException(strategy.backend)
