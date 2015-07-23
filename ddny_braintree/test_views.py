'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import SimpleTestCase

from fillstation.factory import FillFactory
from registration.factory import MemberFactory


class TestDdnyBraintreeViews(SimpleTestCase):
    '''test views'''

    def setUp(self):
        self.member = MemberFactory.create()

    def test_gimme(self):
        ''' test the gimme view when payment verification passes'''
        self.client.logout()
        fills = FillFactory.create_batch(
            10,
            user=self.member.user,
            blender=self.member,
            bill_to=self.member,
        )
        fillz = str([f.id for f in fills])
        amount = sum([f.total_price for f in fills])
        data = {
            "payment_method_nonce": "fake-paypal-one-time-nonce",
            "amount": amount,
            "fillz": fillz,
        }
        response = self.client.post(reverse("braintree:gimme"), data)
        self.assertTemplateUsed(response, "fillstation/payment_success.html")
        self.assertContains(response, "Payment Success")

    def test_gimme_suspicious_operation(self):
        ''' test the gimme view when payment verification passes'''
        self.client.logout()
        fills = FillFactory.create_batch(
            10,
            user=self.member.user,
            blender=self.member,
            bill_to=self.member,
        )
        fillz = str([f.id for f in fills])
        data = {
            "payment_method_nonce": "fake-paypal-one-time-nonce",
            "amount": "-1.00",
            "fillz": fillz,
        }
        response = self.client.post(reverse("braintree:gimme"), data)
        self.assertTemplateUsed(response, "ddny/oops.html")
        self.assertContains(response, "Oops!")
        self.assertContains(response, "Payment amount verification failure.")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "DDNY automated warning: gimme")

    def test_gimme_braintree_error(self):
        ''' test the gimme view when payment verification passes'''
        self.client.logout()
        fills = FillFactory.create_batch(
            10,
            user=self.member.user,
            blender=self.member,
            bill_to=self.member,
        )
        fillz = str([f.id for f in fills])
        amount = sum([f.total_price for f in fills])
        data = {
            "payment_method_nonce": "fake-consumed-nonce",
            "amount": amount,
            "fillz": fillz,
        }
        response = self.client.post(reverse("braintree:gimme"), data)
        self.assertTemplateUsed(response, "ddny/oops.html")
        self.assertContains(response, "Cannot use a payment_method_nonce more than once.")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "DDNY automated warning: gimme")
