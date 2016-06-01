from __future__ import absolute_import, unicode_literals

from .base import *  # NOQA

import os

# ensure we never run in DEBUG mode in production
DEBUG = False
TEMPLATE_DEBUG = False

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

SERVER_EMAIL = os.getenv('CFG_EMAIL_SENDER')
DEFAULT_FROM_EMAIL = os.getenv('CFG_EMAIL_SENDER')
EMAIL_SUBJECT_PREFIX = os.getenv('CFG_EMAIL_PREFIX')

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

# configure logfile handler
LOGGING['handlers']['logfile'] = {
    'level': 'DEBUG',
    'class': 'cloghandler.ConcurrentRotatingFileHandler',
    'filename': os.getenv('CFG_LOG_DIR'),
    'maxBytes': 5242880,  # 5MB
    'backupCount': 5,
    'formatter': 'verbose',
}

# configure opbeat handler
LOGGING['handlers']['opbeat'] = {
    'level': 'WARNING',
    'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
}

# add additional handlers to the root logger
LOGGING['root']['handlers'] += ['logfile', 'opbeat']

# define production loggers (overrides base loggers)
LOGGING['loggers'] = {
    'django': {
        'handlers': ['console', 'logfile'],
        'propagate': True,
    },
    'django.request': {
        'handlers': ['mail_admins', 'logfile', 'opbeat'],
        'level': 'ERROR',
        'propagate': False,
    },
    # Log errors from the Opbeat module to the console (recommended)
    'opbeat.errors': {
        'level': 'ERROR',
        'handlers': ['console'],
        'propagate': False,
    },
}
