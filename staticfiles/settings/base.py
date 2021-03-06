'''Copyright 2015 Downtown Divers New York. All Rights Reserved.'''

import dj_database_url
import os
from oauth2client.service_account import ServiceAccountCredentials
from unipath import Path

from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    '''Get the environment variable name or return an exception'''
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)

BASE_DIR = Path(__file__).ancestor(3)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = get_env_variable('SECRET_KEY')

# Application definition

INSTALLED_APPS = (
    'grappelli',      # this must come before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar', # make stephanie's life easier
    'extra_views',    # Inline forms
    'widget_tweaks',  # add css to form tags
    'ddny',
    'ddny_braintree', # stuff for paying dues and fills
    'ddny_calendar',  # shared events and iCal feed
    'jsignature',     # for the consent form
    # 'debug',          # make stephanie's life easier
    'fillstation',
    'gas',            # gas info duh
    'registration',   # member info
    'tank',           # tank database
)

MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ddny.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        BASE_DIR.child('ddny').child('template'),
        BASE_DIR.child('ddny_braintree').child('template'),
        BASE_DIR.child('ddny_calendar').child('template'),
        BASE_DIR.child('debug').child('template'),
        BASE_DIR.child('fillstation').child('template'),
        BASE_DIR.child('gas').child('template'),
        BASE_DIR.child('registration').child('template'),
        BASE_DIR.child('tank').child('template'),
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
}]

WSGI_APPLICATION = 'ddny.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# I18n
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# Honor the 'X-Forwarded-Proto' header for request.is_secure()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers

ALLOWED_HOSTS = ['.herokuapp.com', '.downtowndivers.org']

# Static asset configuration

STATIC_ROOT = BASE_DIR.child('staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR.child('ddny'),
)

# Settings for django.contrib.auth.

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

# Google calendar api stuff

GOOGLE_CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_dict(
    keyfile_dict={
      'type': 'service_account',
      'project_id': get_env_variable('GOOGLE_PROJECT_ID'),
      'private_key_id': get_env_variable('GOOGLE_PRIVATE_KEY_ID'),
      'private_key': get_env_variable('GOOGLE_PRIVATE_KEY'),
      'client_email': get_env_variable('GOOGLE_CLIENT_EMAIL'),
      'client_id': get_env_variable('GOOGLE_CLIENT_ID'),
      'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
      'token_uri': 'https://oauth2.googleapis.com/token',
      'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
      'client_x509_cert_url': get_env_variable('GOOGLE_CLIENT_X509_CERT_URL'),
    },
    scopes=['https://www.googleapis.com/auth/calendar.events']
)
