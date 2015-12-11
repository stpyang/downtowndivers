'''Copyright 2015 Downtown Divers New York. All Rights Reserved.'''

import dj_database_url
import os
from unipath import Path

from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    '''Get the environment variable name or return an exception'''
    try:
        return os.environ[var_name]
    except KeyError: # pragma: no cover
        error_msg = "Set the {0} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)

BASE_DIR = Path(__file__).ancestor(3)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = get_env_variable("SECRET_KEY")

# Application definition

INSTALLED_APPS = (
    "grappelli",      # this must come before django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",  # make stephanie's life easier
    "jsignature",     # for the consent form
    "widget_tweaks",  # add css to form tags
    "ddny",
    "ddny_braintree", # stuff for paying dues and fills
    "ddny_calendar",  # shared events and iCal feed
    "debug",          # make stephanie's life easier
    "fillstation",
    "gas",            # gas info duh
    "registration",   # member info
    "tank",           # tank database
)

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
)

ROOT_URLCONF = "ddny.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [
        BASE_DIR.child("ddny").child("template"),
        BASE_DIR.child("ddny_braintree").child("template"),
        BASE_DIR.child("ddny_calendar").child("template"),
        BASE_DIR.child("debug").child("template"),
        BASE_DIR.child("fillstation").child("template"),
        BASE_DIR.child("gas").child("template"),
        BASE_DIR.child("registration").child("template"),
        BASE_DIR.child("tank").child("template"),
    ],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ],
    },
}]

WSGI_APPLICATION = "ddny.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# I18n
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "US/Eastern"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# Honor the "X-Forwarded-Proto" header for request.is_secure()

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Allow all host headers

ALLOWED_HOSTS = [".herokuapp.com", ".downtowndivers.org"]

# Static asset configuration

STATIC_ROOT = BASE_DIR.child("staticfiles")

STATIC_URL = "/static/"

STATICFILES_DIRS = (
    BASE_DIR.child("ddny"),
)

# Settings for django.contrib.auth.

LOGIN_URL = "/signin/"

LOGIN_REDIRECT_URL = "/"

