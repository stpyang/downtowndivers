'''Copyright 2015 Downtown Divers New York. All Rights Reserved.'''

import braintree

from .base import *
from .constants import *

DEBUG = False

ALLOWED_HOSTS = ['ddny.herokuapp.com', 'downtowndivers.org']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# DDNY settings

DEFAULT_FROM_EMAIL = 'gizmo.santore@gmail.com'

EMAIL_HOST = 'smtp.sendgrid.net'

EMAIL_HOST_USER = 'ddny'

EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')

EMAIL_PORT = 587

EMAIL_USE_TLS = True

TANK_NAZI = 'raphael.santore@gmail.com'

OOPS_EMAIL = 'stpyang@post.harvard.edu'

# Braintree sandbox

braintree.Configuration.configure(
    braintree.Environment.Production,
    merchant_id=get_env_variable('BRAINTREE_MERCHANT_ID'),
    public_key=get_env_variable('BRAINTREE_PUBLIC_KEY'),
    private_key=get_env_variable('BRAINTREE_PRIVATE_KEY'),
)

BRAINTREE_CLIENT_TOKEN = braintree.ClientToken.generate()
