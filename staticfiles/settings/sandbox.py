'''Copyright 2015 Downtown Divers New York. All Rights Reserved.'''

import braintree

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['ddny-sandbox.herokuapp.com', '127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# DDNY settings

DEFAULT_FROM_EMAIL = 'gizmo.santore@gmail.com'

EMAIL_HOST = 'smtp.sendgrid.net'

EMAIL_HOST_USER = 'ddny'

EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')

EMAIL_PORT = 587

EMAIL_USE_TLS = True

TANK_NAZI = 'stpyang@post.harvard.edu'

OOPS_EMAIL = 'stpyang@post.harvard.edu'

# Braintree sandbox

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    merchant_id=get_env_variable('BRAINTREE_MERCHANT_ID'),
    public_key=get_env_variable('BRAINTREE_PUBLIC_KEY'),
    private_key=get_env_variable('BRAINTREE_PRIVATE_KEY'),
)

BRAINTREE_CLIENT_TOKEN = braintree.ClientToken.generate()
