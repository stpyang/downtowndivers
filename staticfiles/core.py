'''Copyright 2016 DDNY. All Rights Reserved.'''

from decimal import Decimal

from ddny.settings import costs


def cash(money):
    '''Always round to the nearest penny'''
    return Decimal(money).quantize(costs.PENNY)
