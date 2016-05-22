from __future__ import absolute_import, unicode_literals

from .base import *  # NOQA

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ cookiecutter.project_slug }}',
        'USER': '{{ cookiecutter.project_slug }}',
        'PASSWORD': 'some_super_secret_password',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = INSTALLED_APPS + [
    'django_extensions',
    'debug_toolbar'
]

INTERNAL_IPS = ('127.0.0.1', '::1', '10.0.2.2')
