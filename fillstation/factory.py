'''Copyright 2016 DDNY. All Rights Reserved.'''

from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDecimal, FuzzyFloat
from faker import Faker

from registration.factory import MemberFactory, RandomUserFactory
from .models import Fill


FAKE = Faker()

class FillFactory(DjangoModelFactory):
    '''Fill factory for unit tests'''
    class Meta:
        model = Fill

    user = SubFactory(RandomUserFactory)
    blender = SubFactory(MemberFactory)
    bill_to = SubFactory(MemberFactory)
    air_price = FuzzyFloat(low=0.0, high=1.0)
    argon_price = FuzzyFloat(low=0.0, high=1.0)
    helium_price = FuzzyFloat(low=0.0, high=1.0)
    oxygen_price = FuzzyFloat(low=0.0, high=1.0)
    total_price = FuzzyDecimal(low=0.0, high=1.0, precision=2)
    gas_name = FAKE.text(30)
    gas_slug = FAKE.slug()
    tank_code = FAKE.slug()
