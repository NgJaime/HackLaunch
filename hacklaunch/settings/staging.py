from hacklaunch.settings.base import *

DEBUG = False

ALLOWED_HOSTS = [u'ec2-52-74-130-171.ap-southeast-1.compute.amazonaws.com']

AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = 'hacklaunch-images-test'
