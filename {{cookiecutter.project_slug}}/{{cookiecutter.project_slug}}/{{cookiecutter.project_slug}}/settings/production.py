from __future__ import absolute_import, unicode_literals

import os

from .base import *  # NOQA

# Database config
# -----------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': os.getenv('CFG_DB_ENGINE'),
        'NAME': os.getenv('CFG_DB_NAME'),
        'USER': os.getenv('CFG_DB_USER'),
        'HOST': os.getenv('CFG_DB_HOST'),
        'PASSWORD': os.getenv('CFG_DB_PASSWORD'),
        'PORT': '',
    }
}

SECRET_KEY = os.getenv('CFG_SECRET_KEY')

ALLOWED_HOSTS = [os.getenv('CFG_SERVER_NAME'), '127.0.0.1']

# Email config
# -----------------------------------------------------------------------------
SERVER_EMAIL = os.getenv('CFG_EMAIL_SENDER')
DEFAULT_FROM_EMAIL = os.getenv('CFG_EMAIL_SENDER')
EMAIL_SUBJECT_PREFIX = os.getenv('CFG_EMAIL_PREFIX')

# Caching
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('CFG_REDIS_URL'),
        'KEY_PREFIX': os.getenv('CFG_APPNAME'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

MEDIA_ROOT = os.getenv('CFG_MEDIA_DIR')
STATIC_ROOT = os.getenv('CFG_STATIC_DIR')

# Logging
# -----------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
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
        'logfile': {
            'level': 'DEBUG',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'filename': os.getenv('CFG_LOG_DIR'),
            'maxBytes': 5242880,  # 5MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
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
        'handlers': ['console', 'logfile'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logfile'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}

{%- if cookiecutter.opbeat == 'y' -%}
# Opbeat integration
# See https://opbeat.com/languages/django/
# -----------------------------------------------------------------------------
INSTALLED_APPS += ['opbeat.contrib.django']
OPBEAT = {
    'ORGANIZATION_ID': os.getenv('CFG_OPBEAT_ORGANIZATION_ID'),
    'APP_ID': os.getenv('CFG_OPBEAT_APP_ID'),
    'SECRET_TOKEN': os.getenv('CFG_OPBEAT_SECRET_TOKEN'),
}
MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
) + MIDDLEWARE_CLASSES

# configure opbeat handler
LOGGING['handlers']['opbeat'] = {
    'level': 'WARNING',
    'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
}
# Log errors from the Opbeat module to the console (recommended)
LOGGING['loggers']['opbeat.errors'] = {
    'level': 'ERROR',
    'handlers': ['console'],
    'propagate': False,
}
logging['root']['handlers'] += 'opbeat'
{% endif %}
{%- if cookiecutter.sentry == 'y' -%}

# Sentry integration
# See https://docs.getsentry.com/hosted/clients/python/integrations/django/
# -----------------------------------------------------------------------------
SENTRY_DSN = os.getenv('CFG_SENTRY_DSN')
SENTRY_CLIENT = 'raven.contrib.django.raven_compat.DjangoClient'

RAVEN_CONFIG = {
    'DSN': SENTRY_DSN
}

INSTALLED_APPS += ['raven.contrib.django.raven_compat']
RAVEN_MIDDLEWARE = ['raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware']
MIDDLEWARE_CLASSES = RAVEN_MIDDLEWARE + MIDDLEWARE_CLASSES

# configure sentry handler
LOGGING['handlers']['sentry'] = {
    'level': 'ERROR',
    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
}
LOGGING['loggers']['sentry.errors'] = {
    'level': 'ERROR',
    'handlers': ['console'],
    'propagate': False,
}
logging['root']['handlers'] += 'sentry'
{% endif %}
