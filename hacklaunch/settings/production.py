from hacklaunch.settings.base import *

DEBUG = False

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hacklaunch',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}

AWS_S3_SECURE_URLS = True
AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = 'hacklaunch-images-production'

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
