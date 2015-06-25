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

AWS_S3_SECURE_URLS = True
AWS_QUERYSTRING_AUTH = False     
AWS_STORAGE_BUCKET_NAME = 'hacklaunch-images-test'

# Debug staic file settings
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
STATICFILES_DIRS = (os.path.join(os.path.dirname(BASE_DIR), "static", "static")),

#############################
# Django debug toolbar
#############################
DEBUG_TOOLBAR_PANELS = [
    'ddt_request_history.panels.request_history.RequestHistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'ddt_request_history.panels.request_history.allow_ajax',
}

DEBUG_TOOLBAR_CONFIG = {
    'RESULTS_STORE_SIZE': 100,
}
