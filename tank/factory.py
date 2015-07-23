'''Copyright 2015 DDNY. All Rights Reserved.'''

from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyFloat, FuzzyInteger
from faker import Faker

from registration.factory import MemberFactory
from .models import Specification, Tank

FAKE = Faker()

class SpecFactory(DjangoModelFactory):
    class Meta:
        model = Specification

    metal = FuzzyChoice(choices=("Al", "St"))
    name = Sequence(lambda n: "{0}-{1}".format(FAKE.slug(), n))
    slug = Sequence(lambda n: "{0}-{1}".format(FAKE.slug(), n))
    volume = FuzzyFloat(low=6, high=120)
    pressure = FuzzyInteger(low=2400, high=3442)


class TankFactory(DjangoModelFactory):
    class Meta:
        model = Tank

    code = Sequence(lambda n: "{0}-{1}".format(FAKE.slug(), n))
    doubles_code = Sequence(lambda n: "{0}-{1}".format(FAKE.slug(), n))
    spec = SubFactory(SpecFactory)
    serial_number = FuzzyInteger(low=100000, high=999999)
    owner = SubFactory(MemberFactory)
