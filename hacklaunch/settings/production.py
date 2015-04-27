from hacklaunch.settings.base import *

DEBUG = False

ALLOWED_HOSTS = [u'ec2-52-74-151-51.ap-southeast-1.compute.amazonaws.com',
                 u'52.74.151.51',
                 u'www.hacklaunch.com']

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hacklaunch',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
            'sslrootcert': '/home/ubuntu/.ssh/rds-ssl-ca-cert.pem'
        },
    }
}

AWS_S3_SECURE_URLS = True
AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = 'hacklaunch-images-production'

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_SSL_REDIRECT = True
