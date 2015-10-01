'''Copyright 2015 DDNY. All Rights Reserved.'''

from datetime import date
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from factory.fuzzy import FuzzyChoice, FuzzyInteger

from .models import ConsentA, Member, MonthlyDues


FAKE = Faker()
PASSWORD = "password"


class ConsentAFactory(DjangoModelFactory):
    '''Factory boy for consent 1.0'''
    class Meta:
        model = ConsentA

    member_signature = [{"x": [1, 2], "y": [3, 4]}]
    member_signature_date = date.today()
    witness_signature = [{"x": [1, 2], "y": [3, 4]}]
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
    class Meta:
        model = User

    username = Sequence(lambda n: "{0}.{1}".format(FAKE.user_name(), n))
    first_name = FAKE.first_name()
    last_name = FAKE.last_name()
    email = FAKE.email()
    password = make_password(PASSWORD)
    is_superuser = False


class MemberFactory(DjangoModelFactory):
    class Meta:
        model = Member

    user = SubFactory(RandomUserFactory)
    slug = Sequence(lambda n: "{0}_{1}".format(FAKE.slug(), n))
    gender = FuzzyChoice(choices=("male", "female"))
    member_since = date.today()


class MonthlyDuesFactory(DjangoModelFactory):
    class Meta:
        model = MonthlyDues

    member = SubFactory(MemberFactory)
    months = FuzzyInteger(low=0, high=12)
