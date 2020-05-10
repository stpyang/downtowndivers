'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.test import TestCase

from .models import BraintreePaypalDetails, BraintreeTransaction


class TestBraintreeTransactionModel(TestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    def test_is_paid(self):
        '''test the is_paid property for braintree transactions'''
        self.assertTrue(BraintreeTransaction(status='settling').is_paid)
        self.assertTrue(BraintreeTransaction(status='settled').is_paid)
        self.assertFalse(BraintreeTransaction(status='').is_paid)

    def test_paypal_details_string(self):
        '''test the is_paid property for braintree transactions'''
        paypal = BraintreePaypalDetails(payer_email='test@test.com')
        self.assertNotEqual('', str(paypal))
