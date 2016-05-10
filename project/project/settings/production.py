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

ALLOWED_HOSTS = [os.getenv('CFG_SERVER_NAME'), ]

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
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': os.getenv('CFG_LOG_FILE'),
    'maxBytes': 50000,
    'backupCount': 2,
    'formatter': 'standard',
}

# add logfile handler to the root logger
LOGGING['root']['handlers'] += ['logfile']

# define production loggers (overrides base loggers)
LOGGING['loggers'] = {
    'django': {
        'handlers': ['console', 'logfile'],
        'propagate': True,
    },
    'django.request': {
        'handlers': ['mail_admins', 'logfile'],
        'level': 'ERROR',
        'propagate': False,
    },
}
