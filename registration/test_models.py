'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.test import TestCase

from .factory import ConsentAFactory, MemberFactory
from .models import MonthlyDues


class TestMemberModel(TestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    def test_member_stringify(self):
        '''test the stringify method for member models'''
        member = MemberFactory.create()
        self.assertNotEqual('', str(member))

    def test_member_initials(self):
        '''test the stringify method for member models'''
        member = MemberFactory.build(first_name='', last_name='')
        self.assertEqual('', member.initials)
        member = MemberFactory.build(first_name='John', last_name='')
        self.assertEqual('J', member.initials)
        member = MemberFactory.build(first_name='', last_name='Smith')
        self.assertEqual('S', member.initials)
        member = MemberFactory.build(first_name='John', last_name='Smith')
        self.assertEqual('JS', member.initials)


class TestConsentAForm(TestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    def test_consenta_stringify(self):
        '''test that the consent form string is nontrivial'''
        member = MemberFactory.create()
        consent = ConsentAFactory.create(member=member)
        self.assertNotEqual('', str(consent))


class TestMonthlyDuesModel(TestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    def test_monthlydues_stringify(self):
        '''test the paid and unpaid functions'''
        member = MemberFactory.create()
        dues = MonthlyDues.objects.create(member=member, months=1)
        self.assertEqual('{0} dues for 1 month'.format(member.first_name), str(dues))
        dues = MonthlyDues.objects.create(member=member, months=2)
        self.assertEqual('{0} dues for 2 months'.format(member.first_name), str(dues))
