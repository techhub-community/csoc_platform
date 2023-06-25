import os
import sys
from pathlib import Path
from .base import *

from loguru import logger

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

DOMAIN = os.getenv('DOMAIN')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = [DOMAIN, 'django']

CSRF_TRUSTED_ORIGINS = [
    f'https://{DOMAIN}'
]

# EMAIL SETTINGS
EMAIL_BACKEND=os.environ.get('EMAIL_BACKEND')
EMAIL_HOST=os.environ.get('EMAIL_HOST')
EMAIL_PORT=os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER=os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=os.environ.get('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS=os.environ.get('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL=os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_USE_SSL=os.environ.get('EMAIL_USE_SSL')

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT')
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
        "loguru": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": "/app/logs/django.log",  # Change the path as desired
        },
    },
    "root": {
        "handlers": ["console", "loguru"],
        "level": "INFO",
    },
}
