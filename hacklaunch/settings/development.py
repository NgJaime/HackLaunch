from hacklaunch.settings.base import *

DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hacklaunch',
        'USER': 'hacklaunch',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
    }
}

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
)

ALLOWED_HOSTS = []

AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False     
AWS_STORAGE_BUCKET_NAME = 'hacklaunch-images-test'

# Debug staic file settings
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
STATICFILES_DIRS = (os.path.join(os.path.dirname(BASE_DIR), "static", "static")),
