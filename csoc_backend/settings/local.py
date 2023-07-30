import dotenv
import os
from pathlib import Path
from .base import *

dotenv.load_dotenv() 

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", default="c_r-e8v1divj8y+hu@-w=n#$xj#ciuejybd3_(k2h789(mcv8$")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DOMAIN = "localhost:8000"

ALLOWED_HOSTS = ['*','localhost:8000','','64.227.148.114','django']

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000'
]

DOMAIN = 'localhost:8000'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Email Settings
EMAIL_BACKEND=os.getenv('EMAIL_BACKEND')
EMAIL_HOST=os.getenv('EMAIL_HOST')
EMAIL_PORT=os.getenv('EMAIL_PORT')
EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS=os.getenv('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL=os.getenv('DEFAULT_FROM_EMAIL')
EMAIL_USE_SSL=os.getenv('EMAIL_USE_SSL')
EMAIL_USE_TSL=os.getenv('EMAIL_USE_TSL')


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SIMPLE_JWT["SIGNING_KEY"] = SECRET_KEY

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [str(BASE_DIR/"static")]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
