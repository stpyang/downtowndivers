'''Copyright 2020 Downtown Divers New York. All Rights Reserved.'''

from .sandbox import *

DATABASES = {
	'default': {
	    'ENGINE': 'django.db.backends.postgresql_psycopg2',
	    'NAME': 'stpyang',
	    'USER': 'stpyang',
	}
}
