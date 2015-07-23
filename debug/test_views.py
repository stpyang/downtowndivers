'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.test import SimpleTestCase

from django.core.urlresolvers import reverse
from ddny.test_decorators import test_consent_required, test_login_required

from registration.factory import ConsentAFactory, MemberFactory

class TestDebugViews(SimpleTestCase):
    '''test debug views'''

    def setUp(self):
        self.member = MemberFactory.create()
        self.username = self.member.username
        self.password = "password"
        ConsentAFactory.create(member=self.member)

    @test_consent_required(path=reverse("debug:blend_tests"))
    @test_login_required(path=reverse("debug:blend_tests"))
    def test_blend(self):
        '''test the blend_test FBV'''
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(reverse("debug:blend_tests"))
        self.assertTemplateUsed(response, "debug/blend_tests.html")

    @test_consent_required(path=reverse("debug:fill_tests"))
    @test_login_required(path=reverse("debug:fill_tests"))
    def test_fill(self):
        '''test the fill_test FBV'''
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(reverse("debug:fill_tests"))
        self.assertTemplateUsed(response, "debug/fill_tests.html")

    @test_consent_required(path=reverse("debug:todo"))
    @test_login_required(path=reverse("debug:todo"))
    def test_too(self):
        '''test the todo FBV'''
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(reverse("debug:todo"))
        self.assertTemplateUsed(response, "debug/todo.html")
