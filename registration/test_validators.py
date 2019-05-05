'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.core.exceptions import ValidationError
from django.test import TestCase

from .factory import MemberFactory, RandomUserFactory


class TestMemberValidators(TestCase):
    '''test Member validators'''

    def test_validate_user_good(self):
        user = RandomUserFactory.create()
        self.assertEqual(None, MemberFactory.create(user=user).full_clean())

    def test_validate_user_bad(self):
        with self.assertRaises(ValidationError):
            user = RandomUserFactory.create(is_superuser=True)
            MemberFactory.create(user=user).full_clean()
