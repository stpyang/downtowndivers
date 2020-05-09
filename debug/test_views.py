'''Copyright 2016 DDNY. All Rights Reserved.'''

# from django.urls import reverse

# from ddny.test_decorators import test_login_required
# from ddny.test_views import BaseDdnyTestCase


# TODO(stpyang): Fix
# class TestDebugViews(BaseDdnyTestCase):
#     '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

#     @test_consent_required(path=reverse("debug:blend_tests"))
#     @test_login_required(path=reverse("debug:blend_tests"))
#     def test_blend(self):
#         '''test the blend_test FBV'''
#         self.login()
#         response = self.client.get(reverse("debug:blend_tests"))
#         self.assertTemplateUsed(response, "debug/blend_tests.html")

#     @test_consent_required(path=reverse("debug:fill_tests"))
#     @test_login_required(path=reverse("debug:fill_tests"))
#     def test_fill(self):
#         '''test the fill_test FBV'''
#         self.login()
#         response = self.client.get(reverse("debug:fill_tests"))
#         self.assertTemplateUsed(response, "debug/fill_tests.html")

#     @test_consent_required(path=reverse("debug:todo"))
#     @test_login_required(path=reverse("debug:todo"))
#     def test_too(self):
#         '''test the todo FBV'''
#         self.login()
#         response = self.client.get(reverse("debug:todo"))
#         self.assertTemplateUsed(response, "debug/todo.html")
