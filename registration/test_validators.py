'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.core.exceptions import ValidationError
from django.test import TestCase

from .factory import MemberFactory, RandomUserFactory


class TestMemberValidators(TestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    def test_valid_user(self):
        '''test user validation'''
        user = RandomUserFactory.create()
        self.assertEqual(None, MemberFactory.create(user=user).full_clean())

    def test_invalid_user(self):
        '''test user validation'''
        with self.assertRaises(ValidationError):
            user = RandomUserFactory.create(is_superuser=True)
            MemberFactory.create(user=user).full_clean()
