'''Copyright 2015 DDNY. All Rights Reserved.'''

from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDecimal, FuzzyFloat
from faker import Faker

from .models import Gas


FAKE = Faker()

class GasFactory(DjangoModelFactory):
    class Meta:
        model = Gas

    name = Sequence(lambda n: "{0}-{1}".format(FAKE.slug(), n))
    slug = FAKE.slug()
    cost = FuzzyFloat(low=0, high=2)
    argon_percentage = FuzzyDecimal(low=0, high=33, precision=1)
    helium_percentage = FuzzyDecimal(low=0, high=33, precision=1)
    oxygen_percentage = FuzzyDecimal(low=0, high=33, precision=1)
