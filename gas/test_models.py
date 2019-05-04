'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.core.exceptions import ValidationError
from django.test import TestCase

from .factory import GasFactory


class TestGasModel(TestCase):
    '''test gas model'''

    def test_gas_stringify(self):
        '''test the stringify method for gas models'''
        gas = GasFactory.create()
        self.assertNotEqual("", str(gas))

    def test_gas_calculations(self):
        '''test to see if we calculate fraction_* correctly'''
        gas = GasFactory.create()
        self.assertAlmostEqual(
            float(gas.argon_fraction),
            float(gas.argon_percentage) / 100
        )
        self.assertAlmostEqual(
            float(gas.helium_fraction),
            float(gas.helium_percentage) / 100
        )
        self.assertAlmostEqual(
            0.209 * float(gas.air_fraction) + float(gas.oxygen_fraction),
            float(gas.oxygen_percentage) / 100
        )

    def test_gas_clean(self):
        '''test gas cleaning'''
        with self.assertRaises(ValidationError):
            gas = GasFactory.create(
                argon_percentage=50.0,
                helium_percentage=50.0,
                oxygen_percentage=50.0,
                other_percentage=50.0,
            )
            gas.clean()
