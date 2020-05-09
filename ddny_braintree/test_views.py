'''Copyright 2016 DDNY. All Rights Reserved.'''

from decimal import Decimal
from random import randint, random

from django.db.models import Sum
from django.conf import settings
from django.core import mail
from django.urls import reverse

from ddny.test_views import BaseDdnyTestCase
from fillstation.factory import FillFactory
from fillstation.models import Fill, Prepay
from registration.factory import MemberFactory


class TestDdnyBraintreeViews(BaseDdnyTestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

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
        self.assertEqual(count - 10, Fill.objects.unpaid().count())

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

    def test_gimme_prepay(self):
        ''' test the gimme_dues view when payment verification passes'''
        self.client.logout()
        amount = 100 * random()
        data = {
            "payment_method_nonce": "fake-paypal-one-time-nonce",
            "amount": amount,
            "member": self.member.username,
        }
        response = self.client.post(reverse("braintree:gimme_prepay"), data)
        self.assertTemplateUsed(response, "fillstation/payment_success.html")
        self.assertContains(response, "Payment Success")

    def test_gimme_prepay_not_enough(self):
        ''' test the gimme_dues view when payment verification passes'''
        member = MemberFactory.create()

        FillFactory.create_batch(
            2,
            user=member.user,
            blender=member,
            bill_to=member,
            total_price=Decimal(10).quantize(settings.PENNY)
        )

        self.client.logout()
        amount = Decimal(5).quantize(settings.PENNY)
        data = {
            "payment_method_nonce": "fake-paypal-one-time-nonce",
            "amount": amount,
            "member": member.username,
        }
        self.client.post(reverse("braintree:gimme_prepay"), data)

        prepaid = Prepay.objects.filter(member=member)
        total_prepaid = prepaid.aggregate(Sum("amount")).get("amount__sum")
        if total_prepaid is None:
            total_prepaid = Decimal(0.0).quantize(settings.PENNY)

        self.assertEqual(amount, total_prepaid)
        self.assertEqual(0, Fill.objects.paid().filter(bill_to=member).count())
        self.assertEqual(2, Fill.objects.unpaid().filter(bill_to=member).count())

    def test_gimme_prepay_some_enough(self):
        ''' test the gimme_dues view when payment verification passes'''
        member = MemberFactory.create()

        FillFactory.create_batch(
            2,
            user=member.user,
            blender=member,
            bill_to=member,
            total_price=Decimal(10).quantize(settings.PENNY)
        )

        self.client.logout()
        amount = Decimal(15).quantize(settings.PENNY)
        data = {
            "payment_method_nonce": "fake-paypal-one-time-nonce",
            "amount": amount,
            "member": member.username,
        }
        self.client.post(reverse("braintree:gimme_prepay"), data)

        prepaid = Prepay.objects.filter(member=member)
        total_prepaid = prepaid.aggregate(Sum("amount")).get("amount__sum")
        if total_prepaid is None:
            total_prepaid = Decimal(0.0).quantize(settings.PENNY)

        self.assertEqual(amount - 10, total_prepaid)
        self.assertEqual(1, Fill.objects.paid().filter(bill_to=member).count())
        self.assertEqual(1, Fill.objects.unpaid().filter(bill_to=member).count())

    def test_gimme_prepay_enough(self):
        ''' test the gimme_dues view when payment verification passes'''
        member = MemberFactory.create()

        FillFactory.create_batch(
            2,
            user=member.user,
            blender=member,
            bill_to=member,
            total_price=Decimal(10).quantize(settings.PENNY)
        )

        self.client.logout()
        amount = Decimal(20).quantize(settings.PENNY)
        data = {
            "payment_method_nonce": "fake-paypal-one-time-nonce",
            "amount": amount,
            "member": member.username,
        }
        self.client.post(reverse("braintree:gimme_prepay"), data)

        prepaid = Prepay.objects.filter(member=member)
        total_prepaid = prepaid.aggregate(Sum("amount")).get("amount__sum")
        if total_prepaid is None:
            total_prepaid = Decimal(0.0).quantize(settings.PENNY)

        self.assertEqual(Decimal(0).quantize(settings.PENNY), total_prepaid)
        self.assertEqual(2, Fill.objects.paid().filter(bill_to=member).count())
        self.assertEqual(0, Fill.objects.unpaid().filter(bill_to=member).count())

    def test_gimme_prepay_too_much(self):
        ''' test the gimme_dues view when payment verification passes'''
        member = MemberFactory.create()

        FillFactory.create_batch(
            2,
            user=member.user,
            blender=member,
            bill_to=member,
            total_price=Decimal(10).quantize(settings.PENNY)
        )

        self.client.logout()
        amount = Decimal(25).quantize(settings.PENNY)
        data = {
            "payment_method_nonce": "fake-paypal-one-time-nonce",
            "amount": amount,
            "member": member.username,
        }
        self.client.post(reverse("braintree:gimme_prepay"), data)

        prepaid = Prepay.objects.filter(member=member)
        total_prepaid = prepaid.aggregate(Sum("amount")).get("amount__sum")
        if total_prepaid is None:
            total_prepaid = Decimal(0.0).quantize(settings.PENNY)

        self.assertEqual(amount - 20, total_prepaid)
        self.assertEqual(2, Fill.objects.paid().filter(bill_to=member).count())
        self.assertEqual(0, Fill.objects.unpaid().filter(bill_to=member).count())
