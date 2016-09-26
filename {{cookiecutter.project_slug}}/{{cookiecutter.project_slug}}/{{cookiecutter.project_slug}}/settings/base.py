"""
Django settings for {{ cookiecutter.project_name }}
"""

from __future__ import absolute_import, unicode_literals

import os
from os import path

PROJECT_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
BASE_DIR = path.dirname(PROJECT_DIR)

# DEBUG
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
# ------------------------------------------------------------------------------
DEBUG = False

# App config
# -----------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin
    'django.contrib.admin',
]

THIRD_PARTY_APPS = []

LOCAL_APPS = []

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware config
# -----------------------------------------------------------------------------
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Template config
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
# -----------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path.join(PROJECT_DIR, 'templates')
        ],
        'OPTIONS': {
            'debug': False,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = '{{ cookiecutter.project_slug }}.urls'

WSGI_APPLICATION = '{{ cookiecutter.project_slug }}.wsgi.application'

# Database confg
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# -----------------------------------------------------------------------------
DATABASES = {}

# Authentication Configuration
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization config
# https://docs.djangoproject.com/en/1.9/topics/i18n/
# -----------------------------------------------------------------------------
LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# -----------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, 'public', 'static')
STATICFILES_DIRS = (path.join(BASE_DIR, 'tmp', 'static'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Media config
# -----------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = path.join(BASE_DIR, 'public', 'media')

{%- if cookiecutter.wagtail == "y" %}
# Wagtail
# -----------------------------------------------------------------------------
WAGTAIL_APPS = [
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

    'modelcluster',
    'taggit',
]
INSTALLED_APPS = WAGTAIL_APPS + INSTALLED_APPS

MIDDLEWARE_CLASSES += [
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware']

WAGTAIL_SITE_NAME = "{{ cookiecutter.project_name }}"

# Base URL to use when referring to full URLs within the Wagtail admin backend
# (e.g. in notification emails). Don't include '/admin' or a trailing slash.
BASE_URL = 'http://{{ cookiecutter.domain_name }}'

# Use Elasticsearch as the search backend for extra performance and better
# search results
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch',
        'INDEX': '{{ cookiecutter.project_slug }}',
    },
}
{% endif -%}
