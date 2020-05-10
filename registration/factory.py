'''Copyright 2016 DDNY. All Rights Reserved.'''

from datetime import date
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from faker import Faker

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from .models import ConsentA, Member


FAKE = Faker()
PASSWORD = 'password'


class ConsentAFactory(DjangoModelFactory):
    '''https://factoryboy.readthedocs.io/en/latest/orms.html#the-djangomodelfactory-subclass'''

    class Meta:
        '''https://factoryboy.readthedocs.io/en/latest/reference.html'''

        model = ConsentA

    member_signature = [{'x': [1, 2], 'y': [3, 4]}]
    member_signature_date = date.today()
    witness_signature = [{'x': [1, 2], 'y': [3, 4]}]
    witness_signature_date = date.today()
    consent_is_experienced_certified_diver = True
    consent_club_is_non_profit = True
    consent_vip_tank = True
    consent_examine_tank = True
    consent_no_unsafe_tank = True
    consent_analyze_gas = True
    consent_compressed_gas_risk = True
    consent_diving_risk = True
    consent_sole_responsibility = True
    consent_do_not_sue = True
    consent_strenuous_activity_risk = True
    consent_inspect_equipment = True
    consent_lawful_age = True
    consent_release_of_risk = True


class RandomUserFactory(DjangoModelFactory):
    '''https://factoryboy.readthedocs.io/en/latest/orms.html#the-djangomodelfactory-subclass'''

    class Meta:
        '''https://factoryboy.readthedocs.io/en/latest/reference.html'''

        model = User

    username = Sequence(lambda n: '{}.{}'.format(FAKE.user_name(), n))  # pylint: disable=no-member
    first_name = FAKE.first_name()  # pylint: disable=no-member
    last_name = FAKE.last_name()  # pylint: disable=no-member
    email = FAKE.email()  # pylint: disable=no-member
    password = make_password(PASSWORD)
    is_superuser = False


class MemberFactory(DjangoModelFactory):
    '''https://factoryboy.readthedocs.io/en/latest/orms.html#the-djangomodelfactory-subclass'''

    class Meta:
        '''https://factoryboy.readthedocs.io/en/latest/reference.html'''

        model = Member

    user = SubFactory(RandomUserFactory)
    slug = Sequence(lambda n: '{0}_{1}'.format(FAKE.slug(), n))  # pylint: disable=no-member
    gender = FuzzyChoice(choices=('male', 'female'))
    member_since = date.today()
