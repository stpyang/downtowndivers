'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.test import SimpleTestCase

from .models import BraintreeTransaction


class BraintreeTransactionModel(SimpleTestCase):
    '''test braintree transaction model'''

    def test_is_paid(self):
        '''test the is_paid property for braintree transactions'''
        self.assertTrue(BraintreeTransaction(status="settling").is_paid)
        self.assertTrue(BraintreeTransaction(status="settled").is_paid)
        self.assertFalse(BraintreeTransaction(status="").is_paid)
