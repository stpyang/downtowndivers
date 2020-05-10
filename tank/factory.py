'''Copyright 2016 DDNY. All Rights Reserved.'''

from datetime import date as datetime_date

from django.utils.text import slugify
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyFloat, FuzzyInteger
from faker import Faker

from registration.factory import MemberFactory
from .models import Specification, Tank, Vip

FAKE = Faker()


class SpecFactory(DjangoModelFactory):
    '''https://factoryboy.readthedocs.io/en/latest/orms.html#the-djangomodelfactory-subclass'''

    class Meta:
        '''https://factoryboy.readthedocs.io/en/latest/reference.html'''

        model = Specification

    material = FuzzyChoice(choices=('Aluminum', 'Steel'))
    name = Sequence(lambda n: '{0}-{1}'.format(FAKE.slug(), n))  # pylint: disable=no-member
    slug = slugify(name)
    volume = FuzzyFloat(low=6, high=120)
    working_pressure = FuzzyInteger(low=2400, high=3442)


class TankFactory(DjangoModelFactory):
    '''https://factoryboy.readthedocs.io/en/latest/orms.html#the-djangomodelfactory-subclass'''

    class Meta:
        '''https://factoryboy.readthedocs.io/en/latest/reference.html'''

        model = Tank

    code = Sequence(lambda n: '{0}-{1}'.format(FAKE.slug(), n))  # pylint: disable=no-member
    doubles_code = Sequence(lambda n: '{0}-{1}'.format(FAKE.slug(), n))  # pylint: disable=no-member
    spec = SubFactory(SpecFactory)
    serial_number = FuzzyInteger(low=100000, high=999999)
    owner = SubFactory(MemberFactory)


class VipFactory(DjangoModelFactory):
    '''https://factoryboy.readthedocs.io/en/latest/orms.html#the-djangomodelfactory-subclass'''

    class Meta:
        '''https://factoryboy.readthedocs.io/en/latest/reference.html'''

        model = Vip

    tank = SubFactory(TankFactory)
    date = datetime_date.today()
    tank_owners_name = FAKE.name()  # pylint: disable=no-member
