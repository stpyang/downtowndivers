'''Copyright 2016 DDNY. All Rights Reserved.'''

from random import randint

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase

from fillstation.models import Fill
from gas.factory import GasFactory
from registration.factory import MemberFactory
from tank.factory import SpecFactory, TankFactory
from .factory import FillFactory
from .models import _build_fill


class TestFillModel(TestCase):
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
            other_percentage=0,
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
        total_price = fill.cubic_feet * (float(settings.AIR_COST + settings.EQUIPMENT_COST_PROPORTIONAL))
        self.assertAlmostEqual(total_price, float(fill.total_price))

    def test_clean_bad_blender(self):
        with self.assertRaises(ValidationError):
            member = MemberFactory.create()
            member.is_blender = False
            FillFactory.create(blender=member).clean()

    def test_clean_bad_psi(self):
        with self.assertRaises(ValidationError):
            member = MemberFactory.create()
            member.is_blender = True
            FillFactory.create(blender=member, psi_start=100, psi_end=0).clean()

    def test_clean_good(self):
        member = MemberFactory.create(is_blender=True)
        self.assertEqual(None, FillFactory.create(
            blender=member,
            psi_start=0,
            psi_end=100,
        ).clean())
        self.assertEqual(None, FillFactory.create(
            blender=member,
            gas_name=None,
            gas_slug=None,
            air_price=0.0,
            argon_price=0.0,
            helium_price=0.0,
            oxygen_price=0.0,
            is_equipment_surcharge=True,
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
        self.assertEqual(True, fill.is_paid)

    def test_fill_manager(self):
        '''test the paid and unpaid functions'''
        paid_count = Fill.objects.paid().count()
        unpaid_count = Fill.objects.unpaid().count()
        self.assertEqual(Fill.objects.count(), paid_count + unpaid_count)
        paid_num = randint(0, 10)
        unpaid_num = randint(0, 10)
        FillFactory.create_batch(paid_num, is_paid=True)
        FillFactory.create_batch(unpaid_num, is_paid=False)
        self.assertEqual(paid_count + paid_num, Fill.objects.paid().count())
        self.assertEqual(unpaid_count + unpaid_num, Fill.objects.unpaid().count())
