from __future__ import absolute_import, unicode_literals

from .base import *  # NOQA

# Debug
# ------------------------------------------------------------------------------
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Secret config
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = 'CHANGEME!!!'

# Database config
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# -----------------------------------------------------------------------------
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

# django-dbug-toolbar
# -----------------------------------------------------------------------------
INSTALLED_APPS += ['debug_toolbar']
INTERNAL_IPS = ('127.0.0.1', '::1', '10.0.2.2')

# django-extensions
# -----------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions']


# Mail settings
# -----------------------------------------------------------------------------
EMAIL_PORT = 1025
EMAIL_HOST = 'localhost'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Caching
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}
