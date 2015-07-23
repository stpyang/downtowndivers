'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from .factory import MemberFactory, RandomUserFactory


class TestMemberValidators(SimpleTestCase):
    '''test Member validators'''

    def test_validate_user_good(self):
        user = RandomUserFactory.create()
        self.assertEquals(None, MemberFactory.create(user=user).full_clean())

    def test_validate_user_bad(self):
        with self.assertRaises(ValidationError):
            user = RandomUserFactory.create(is_superuser=True)
            MemberFactory.create(user=user).full_clean()
