'''Copyright 2016 DDNY. All Rights Reserved.'''

from decimal import Decimal

from django.conf import settings

def cash(money):
    return Decimal(money).quantize(settings.PENNY)
