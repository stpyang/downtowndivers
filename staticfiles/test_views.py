'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.contrib.messages.constants import WARNING
from django.test import TestCase
from django.urls import reverse

from registration.factory import (
    ConsentAFactory, MemberFactory, RandomUserFactory
    )
from .test_decorators import test_consent_required, test_login_required


class BaseDdnyTestCase(TestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    def setUp(self):
        self.member = MemberFactory.create()
        self.username = self.member.username
        self.password = 'password'
        self.user = self.member.user
        self.consent = ConsentAFactory.create(member=self.member)

    def login(self):
        '''log in with our test member'''
        self.assertTrue(
            self.client.login(username=self.username, password=self.password)
        )


class TestDdnyViews(BaseDdnyTestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    def test_contact_info(self):
        ''' test the contact_info view '''
        response = self.client.get(reverse('contact_info'))
        self.assertTemplateUsed(response, 'ddny/contact_info.html')

    @test_consent_required(path=reverse('home'))
    @test_login_required(path=reverse('home'))
    def test_home(self):
        ''' test the home view '''
        self.assertEqual(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'ddny/home.html')
        self.assertContains(
            response,
            'Hello, {0}!'.format(self.user.first_name)
        )
        messages = list(response.context['messages'])
        self.assertEqual(0, len(messages))

    @test_consent_required(path=reverse('home'))
    @test_login_required(path=reverse('home'))
    def test_home_superuser(self):
        ''' test the home view '''
        user = RandomUserFactory.create(is_superuser=True)
        self.assertEqual(
            True,
            self.client.login(username=user.username, password='password')
        )
        response = self.client.get(reverse('home'), follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, WARNING)

    def test_club_dues(self):
        ''' test the club_dues view '''
        response = self.client.get(reverse('club_dues'))
        self.assertTemplateUsed(response, 'ddny/club_dues.html')

    def test_privacy_policy(self):
        ''' test the privacy_policy view '''
        response = self.client.get(reverse('privacy_policy'))
        self.assertTemplateUsed(response, 'ddny/privacy_policy.html')

    def test_refund_policy(self):
        ''' test the refund_policy view '''
        response = self.client.get(reverse('refund_policy'))
        self.assertTemplateUsed(response, 'ddny/refund_policy.html')
