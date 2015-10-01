'''Copyright 2015 DDNY. All Rights Reserved.'''

from random import randint

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from fillstation.models import Fill
from gas.factory import GasFactory
from registration.factory import MemberFactory
from tank.factory import SpecFactory, TankFactory
from .factory import FillFactory
from .models import _build_fill


class TestFillModel(SimpleTestCase):
    '''test fill model'''

    def test_fill_string(self):
        '''test stringify method for fill model'''
        fill = FillFactory.create()
        self.assertNotEqual("", str(fill))

    def test_build_fill(self):
        '''test cubic_feet and gas_price calculations '''
        member = MemberFactory.create()
        spec = SpecFactory.create(working_pressure=100, volume=2.0)
        tank = TankFactory.create(spec=spec)
        gas = GasFactory.create(
            argon_percentage=0,
            helium_percentage=0,
            oxygen_percentage=20.9,
        )
        fill = _build_fill(
            username=member.username,
            blender=member.username,
            bill_to=member.username,
            tank_code=tank.code,
            gas_name=gas.name,
            psi_start=0,
            psi_end=400,
            is_blend=False,
        )
        fill.save()
        self.assertAlmostEqual(8.0, fill.cubic_feet)
        gas_price = fill.cubic_feet * float(settings.AIR_COST)
        self.assertAlmostEqual(gas_price, fill.gas_price)

    def test_clean_bad_blender(self):
        with self.assertRaises(ValidationError):
            member = MemberFactory.create()
            member.is_blender = False
            FillFactory.create(blender=member).clean()

    def test_clean_bad_psi(self):
        with self.assertRaises(ValidationError):
            member = MemberFactory.create()
            member.is_blender = True
            FillFactory.create(blender=member, psi_start=1, psi_end=0).clean()

    def test_clean_good(self):
        member = MemberFactory.create(is_blender=True)
        self.assertEquals(None, FillFactory.create(
            blender=member,
            psi_start=0,
            psi_end=1,
        ).clean())

    def test_autopay_fills(self):
        '''test that the log_fill view works'''
        raph = MemberFactory.create(autopay_fills=True)
        spec = SpecFactory.create()
        tank = TankFactory.create(spec=spec)
        gas = GasFactory.create(
            argon_percentage=0,
            helium_percentage=0,
            oxygen_percentage=20.9,
        )
        fill = _build_fill(
            username=raph.username,
            blender=raph.username,
            bill_to=raph.username,
            tank_code=tank.code,
            gas_name=gas.name,
            psi_start=0,
            psi_end=400,
            is_blend=False,
        )
        fill.save()
        self.assertEquals(True, fill.is_paid)

    def test_fill_manager(self):
        '''test the paid and unpaid functions'''
        paid_count = Fill.objects.paid().count()
        unpaid_count = Fill.objects.unpaid().count()
        self.assertEquals(Fill.objects.count(), paid_count + unpaid_count)
        p = randint(0, 10)
        u = randint(0, 10)
        FillFactory.create_batch(p, is_paid=True)
        FillFactory.create_batch(u, is_paid=False)
        self.assertEquals(paid_count + p, Fill.objects.paid().count())
        self.assertEquals(unpaid_count + u, Fill.objects.unpaid().count())
