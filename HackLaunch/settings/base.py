"""
Django settings for HackLaunch project.

Generated by 'django-admin startproject' using Django 1.8a1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from hackLaunch.settings.keys import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+-xy1ms)g8&t98uv9zg4(1ot-yyq&64tmx(+@pj2u=42ov2u0l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'zxcvbn_password',
    'widget_tweaks',
    'storages',
]

PROJECT_APPS = [
    'users'
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

ROOT_URLCONF = 'hackLaunch.urls'

LOGIN_REDIRECT_URL = '/'
# todo
LOGIN_URL = 'django.contrib.auth.views.login'

TEMPLATE_DIRS = (
    'templates',
    'base/templates',
    'users/templates'
)

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': ['templates', 'base/templates', 'users/templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#                 'social.apps.django_app.context_processors.backends',
#                 'social.apps.django_app.context_processors.login_redirect',
#
#             ],
#         },
#     },
# ]


if DEBUG:
    MEDIA_URL = '/media/'
    STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
    STATICFILES_DIRS = (os.path.join(os.path.dirname(BASE_DIR), "static", "static")),
    # TEMPLATES['OPTIONS']['context_processors']  'django.core.context_processors.static'


WSGI_APPLICATION = 'hackLaunch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hacklaunch',
        'USER': 'hacklaunch',
        'PASSWORD': 'password',
        'HOST': 'localhost'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'hacklaunch.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'base': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'hacklaunch': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'users': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128
PASSWORD_MIN_ENTROPY = 25

#############################
# Python social auth settings
#############################
AUTH_USER_MODEL = 'users.User'
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

AUTHENTICATION_BACKENDS = (
    'social.backends.bitbucket.BitbucketOAuth',
    'social.backends.email.EmailAuth',
    'social.backends.github.GithubOAuth2',
    'social.backends.linkedin.LinkedinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'users.pipeline.require_email',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'users.pipeline.user_password',
    'social.pipeline.social_auth.associate_user',
    'users.pipeline.load_extra_data',
    'social.pipeline.user.user_details'
)

SOCIAL_AUTH_FORCE_POST_DISCONNECT = True
SOCIAL_AUTH_FORCE_EMAIL_VALIDATION = True
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'users.mail.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/validation_sent/'
EMAIL_FROM = 'noreply@hacklaunch.com'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'home.html'
USERNAME_IS_FULL_EMAIL = True
# SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
SOCIAL_AUTH_EMAIL_FORM_URL = '/'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/profile/'

SOCIAL_AUTH_BACKEND_ERROR_URL = '/new-error-url/'

SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'


#############################
# Social auth providers
#############################

# Add email to requested authorizations.
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']

# Add the fields so they will be requested from linkedin.
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email-address', 'headline', 'industry', 'location', 'specialties', 'picture-url']

# Arrange to add the fields to UserSocialAuth.extra_data
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [('id', 'id'),
                                   ('firstName', 'first_name'),
                                   ('lastName', 'last_name'),
                                   ('emailAddress', 'email_address'),
                                   ('headline', 'headline'),
                                   ('industry', 'industry'),
                                   ('location', 'location'),
                                   ('specialties', 'specialties'),
                                   ('picture-url', 'picture-url'),
                                   ('public-profile-url', 'public-profile-url')]


#############################
# S3 base
#############################
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


#############################
# Image resizing
#############################
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 99
DJANGORESIZED_DEFAULT_KEEP_META = True
MAX_IMAGE_SIZE = 5*1024*1024

