from hacklaunch.settings.base import *

DEBUG = False

ALLOWED_HOSTS = [u'ec2-52-74-130-171.ap-southeast-1.compute.amazonaws.com',
		         u'52.74.32.193',
		         u'staging.hacklaunch.com']

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


AWS_S3_SECURE_URLS = True
AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = 'hacklaunch-images-test'

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_SSL_REDIRECT = True
EMAIL_USE_TLS = True

INSTALLED_APPS += (
    "opbeat.contrib.django",
)

OPBEAT = {
    "ORGANIZATION_ID": "e77b976a46304abc8dbdb02e617237c8",
    "APP_ID": "7c47c1556b",
    "SECRET_TOKEN": "62a9fefe916b83ca4c5109f534c0060a4065082a"
}

MIDDLEWARE_CLASSES += (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',

)

#############################
# django-haystack
#############################
# realtime update to the elastic search server
# todo better to customise this to limit call to when they are needed
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
