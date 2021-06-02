'''Copyright 2020 Downtown Divers New York. All Rights Reserved.'''

from .sandbox import *

DEBUG = True

DATABASES = {
	'default': {
	    'ENGINE': 'django.db.backends.postgresql_psycopg2',
	    'NAME': 'stpyang',
	    'USER': 'stpyang',
	}
}

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
    'debug',
)
