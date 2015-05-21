from hacklaunch.settings.base import *

DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hacklaunch-test',
        'USER': 'hacklaunch',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
    }
}

INSTALLED_APPS += ['django_jenkins']

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_csslint',
)
