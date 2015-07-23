'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.test import SimpleTestCase

from .factory import ConsentAFactory, MemberFactory


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
