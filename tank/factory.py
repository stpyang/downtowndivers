'''Copyright 2015 DDNY. All Rights Reserved.'''

from datetime import date as datetime_date

from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyFloat, FuzzyInteger
from faker import Faker

from registration.factory import MemberFactory
from .models import Specification, Tank, Vip

FAKE = Faker()

class SpecFactory(DjangoModelFactory):
    class Meta:
        model = Specification

    material = FuzzyChoice(choices=("Aluminum", "Steel"))
    name = Sequence(lambda n: "{0}-{1}".format(FAKE.slug(), n))
    slug = Sequence(lambda n: "{0}-{1}".format(FAKE.slug(), n))
    volume = FuzzyFloat(low=6, high=120)
    working_pressure = FuzzyInteger(low=2400, high=3442)


class TankFactory(DjangoModelFactory):
    class Meta:
        model = Tank

    code = Sequence(lambda n: "{0}-{1}".format(FAKE.slug(), n))
    doubles_code = Sequence(lambda n: "{0}-{1}".format(FAKE.slug(), n))
    spec = SubFactory(SpecFactory)
    serial_number = FuzzyInteger(low=100000, high=999999)
    owner = SubFactory(MemberFactory)


class VipFactory(DjangoModelFactory):
    class Meta:
        model = Vip

    tank = SubFactory(TankFactory)
    date = datetime_date.today()
    tank_owners_name = FAKE.name()
