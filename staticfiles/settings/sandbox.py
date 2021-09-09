'''Copyright 2015 Downtown Divers New York. All Rights Reserved.'''

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['ddny-sandbox.herokuapp.com', '127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# DDNY settings

DEFAULT_FROM_EMAIL = 'gizmo.santore@gmail.com'

SENDGRID_API_KEY = get_env_variable('SENDGRID_API_KEY')

EMAIL_HOST = 'smtp.sendgrid.net'

EMAIL_HOST_USER = 'apikey'

EMAIL_HOST_PASSWORD = SENDGRID_API_KEY

EMAIL_PORT = 587

EMAIL_USE_TLS = True

TANK_NAZI = 'stpyang@post.harvard.edu'

OOPS_EMAIL = 'stpyang@post.harvard.edu'
