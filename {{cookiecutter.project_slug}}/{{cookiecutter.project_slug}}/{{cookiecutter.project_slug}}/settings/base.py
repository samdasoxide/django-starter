"""
Django settings for {{ cookiecutter.project_name }}
"""

from __future__ import absolute_import, unicode_literals

import os
from os import path

PROJECT_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
BASE_DIR = path.dirname(PROJECT_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hz$#y8##*6s+vyo_jbwl0%=ks3z#wz5r(x)#r(gnj5d^gcpfbo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['{{ cookiecutter.domain_name }}']


# Application definition

INSTALLED_APPS = [
{%- if cookiecutter.wagtail == "y" %}
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
{% endif %}
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'opbeat.contrib.django',
]

MIDDLEWARE_CLASSES = [
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
{%- if cookiecutter.wagtail == "y" %}
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
{% endif %}
]

ROOT_URLCONF = '{{ cookiecutter.project_slug }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path.join(PROJECT_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '{{ cookiecutter.project_slug }}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {}


# Password validation
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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = path.join(BASE_DIR, 'public', 'static')

STATICFILES_DIRS = (
    path.join(BASE_DIR, 'tmp', 'static'),
)

MEDIA_URL = '/media/'

MEDIA_ROOT = path.join(BASE_DIR, 'public', 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

OPBEAT = {
    'ORGANIZATION_ID': os.getenv('CFG_OPBEAT_ORGANIZATION_ID'),
    'APP_ID': os.getenv('CFG_OPBEAT_APP_ID'),
    'SECRET_TOKEN': os.getenv('CFG_OPBEAT_SECRET_TOKEN'),
}

{%- if cookiecutter.wagtail == "y" %}

# Wagtail settings

WAGTAIL_SITE_NAME = "{{ cookiecutter.project_name }}"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://{{ cookiecutter.domain_name }}'

# Use Elasticsearch as the search backend for extra performance and better
# search results

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'INDEX': '{{ cookiecutter.project_slug }}',
    },
}
{% endif -%}
