'''Copyright 2015 DDNY. All Rights Reserved.'''

from random import randint

from django.test import SimpleTestCase

from .factory import ConsentAFactory, MemberFactory, MonthlyDuesFactory
from .models import MonthlyDues


class TestMemberModel(SimpleTestCase):
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


class TestConsentAForm(SimpleTestCase):

    def test_consenta_stringify(self):
        member = MemberFactory.create()
        consent = ConsentAFactory.create(member=member)
        self.assertNotEqual("", str(consent))

class TestMonthlyDuesModel(SimpleTestCase):

    def test_monthlydues_manager(self):
        '''test the paid and unpaid functions'''
        paid_count = MonthlyDues.objects.paid().count()
        unpaid_count = MonthlyDues.objects.unpaid().count()
        self.assertEquals(MonthlyDues.objects.count(), paid_count + unpaid_count)
        p = randint(0, 10)
        u = randint(0, 10)
        MonthlyDuesFactory.create_batch(p, is_paid=True)
        MonthlyDuesFactory.create_batch(u, is_paid=False)
        self.assertEquals(paid_count + p, MonthlyDues.objects.paid().count())
        self.assertEquals(unpaid_count + u, MonthlyDues.objects.unpaid().count())
