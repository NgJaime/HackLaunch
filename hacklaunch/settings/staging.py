from hacklaunch.settings.base import *

DEBUG = False

ALLOWED_HOSTS = [u'ec2-52-74-130-171.ap-southeast-1.compute.amazonaws.com',
		         u'52.74.32.193',
		         u'staging.hacklaunch.com']

AWS_S3_SECURE_URLS = True
AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = 'hacklaunch-images-test'

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_SSL_REDIRECT = True
EMAIL_USE_TLS = True
