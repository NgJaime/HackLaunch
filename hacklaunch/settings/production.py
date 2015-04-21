from hacklaunch.settings.base import *

DEBUG = False

ALLOWED_HOSTS = []

AWS_S3_SECURE_URLS = True
AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = 'hacklaunch-images-production'

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
