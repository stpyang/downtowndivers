'''Copyright 2016 DDNY. All Rights Reserved.'''

from random import randint

from django.test import TestCase

from .factory import ConsentAFactory, MemberFactory, MonthlyDuesFactory
from .models import MonthlyDues


class TestMemberModel(TestCase):
    '''test gas model'''

    def test_member_stringify(self):
        '''test the stringify method for member models'''
        member = MemberFactory.create()
        self.assertNotEqual("", str(member))

    def test_member_initials(self):
        '''test the stringify method for member models'''
        member = MemberFactory.build(first_name="", last_name="")
        self.assertEqual("", member.initials)
        member = MemberFactory.build(first_name="John", last_name="")
        self.assertEqual("J", member.initials)
        member = MemberFactory.build(first_name="", last_name="Smith")
        self.assertEqual("S", member.initials)
        member = MemberFactory.build(first_name="John", last_name="Smith")
        self.assertEqual("JS", member.initials)

class TestConsentAForm(TestCase):

    def test_consenta_stringify(self):
        member = MemberFactory.create()
        consent = ConsentAFactory.create(member=member)
        self.assertNotEqual("", str(consent))

class TestMonthlyDuesModel(TestCase):
    '''test the monthly dues model'''

    def test_monthlydues_manager(self):
        '''test the paid and unpaid functions'''
        paid_count = MonthlyDues.objects.paid().count()
        unpaid_count = MonthlyDues.objects.unpaid().count()
        self.assertEqual(MonthlyDues.objects.count(), paid_count + unpaid_count)
        p = randint(0, 10)
        u = randint(0, 10)
        MonthlyDuesFactory.create_batch(p, is_paid=True)
        MonthlyDuesFactory.create_batch(u, is_paid=False)
        self.assertEqual(paid_count + p, MonthlyDues.objects.paid().count())
        self.assertEqual(unpaid_count + u, MonthlyDues.objects.unpaid().count())

    def test_monthlydues_stringify(self):
        '''test the paid and unpaid functions'''
        member = MemberFactory.create()
        dues = MonthlyDues.objects.create(member=member, months=1)
        self.assertEqual("{0} dues for 1 month".format(member.first_name), str(dues))
        dues = MonthlyDues.objects.create(member=member, months=2)
        self.assertEqual("{0} dues for 2 months".format(member.first_name), str(dues))
