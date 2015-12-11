'''Copyright 2016 DDNY. All Rights Reserved.'''

from random import randint

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse

from ddny.test_views import BaseDdnyTestCase
from fillstation.factory import FillFactory
from fillstation.models import Fill


class TestDdnyBraintreeViews(BaseDdnyTestCase):
    '''test that pages load correctly'''

    def test_gimme_fills(self):
        ''' test the gimme_fills view when payment verification passes'''
        self.client.logout()
        fills = FillFactory.create_batch(
            10,
            user=self.member.user,
            blender=self.member,
            bill_to=self.member,
        )
        count = Fill.objects.unpaid().count()
        fillz = str([f.id for f in fills])
        amount = sum([f.total_price for f in fills])
        data = {
            "payment_method_nonce": "fake-paypal-one-time-nonce",
            "fillz": fillz,
            "amount": amount,
        }
        response = self.client.post(reverse("braintree:gimme_fills"), data)
        self.assertTemplateUsed(response, "fillstation/payment_success.html")
        self.assertContains(response, "Payment Success")
        self.assertEquals(count - 10, Fill.objects.unpaid().count())

    def test_gimme_fills_suspicious_operation(self):
        ''' test the gimme_fills view when payment verification passes'''
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
            "fillz": fillz,
            "amount": "-1.00",
        }
        response = self.client.post(reverse("braintree:gimme_fills"), data)
        self.assertTemplateUsed(response, "ddny/oops.html")
        self.assertContains(response, "Oops!")
        self.assertContains(response, "Payment amount verification failure.")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "DDNY automated warning: gimme_fills")

    def test_gimme_fills_braintree_error(self):
        ''' test the gimme_fills view when payment verification passes'''
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
            "fillz": fillz,
            "amount": amount,
        }
        response = self.client.post(reverse("braintree:gimme_fills"), data)
        self.assertTemplateUsed(response, "ddny/oops.html")
        self.assertContains(response, "Cannot use a payment_method_nonce more than once.")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "DDNY automated warning: gimme_fills")

    def test_gimme_dues(self):
        ''' test the gimme_dues view when payment verification passes'''
        self.client.logout()
        months = 1 + randint(0, 12)
        amount = months * settings.MONTHLY_DUES
        data = {
            "payment_method_nonce": "fake-paypal-one-time-nonce",
            "months": months,
            "amount": amount,
            "member": self.member.username,
        }
        response = self.client.post(reverse("braintree:gimme_dues"), data)
        self.assertTemplateUsed(response, "fillstation/payment_success.html")
        self.assertContains(response, "Payment Success")

    def test_gimme_dues_suspicious_operation(self):
        ''' test the gimme_dues view when payment verification passes'''
        self.client.logout()
        months = 1 + randint(0, 12)
        data = {
            "payment_method_nonce": "fake-paypal-one-time-nonce",
            "months": months,
            "amount": "-1.00",
            "member": self.member.username,
        }
        response = self.client.post(reverse("braintree:gimme_dues"), data)
        self.assertTemplateUsed(response, "ddny/oops.html")
        self.assertContains(response, "Oops!")
        self.assertContains(response, "Payment amount verification failure.")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "DDNY automated warning: gimme_dues")

    def test_gimme_dues_braintree_error(self):
        ''' test the gimme_dues view when payment verification passes'''
        self.client.logout()
        months = 1 + randint(0, 12)
        amount = months * settings.MONTHLY_DUES
        data = {
            "payment_method_nonce": "fake-consumed-nonce",
            "months": months,
            "amount": amount,
            "member": self.member.username,
        }
        response = self.client.post(reverse("braintree:gimme_dues"), data)
        self.assertTemplateUsed(response, "ddny/oops.html")
        self.assertContains(response, "Cannot use a payment_method_nonce more than once.")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "DDNY automated warning: gimme_dues")
