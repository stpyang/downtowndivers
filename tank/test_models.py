'''Copyright 2016 DDNY. All Rights Reserved.'''

from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from registration.factory import MemberFactory
from .factory import SpecFactory, TankFactory
from .models import Hydro, Tank, Vip


class TestSpecificationModel(TestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    def test_spec_string(self):
        '''test that the stringify method for the Spec model still works'''

        spec = SpecFactory.build()
        self.assertNotEqual('', str(spec))

    def test_tank_factor(self):
        '''the tank factor is the number of cubic feet per 100 psi'''

        spec = SpecFactory.build(
            volume=1,
            working_pressure=100,
        )
        self.assertEqual(1, spec.tank_factor)


class TestTankModel(TestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    def test_tank_string(self):
        '''test that the stringify method for the Tank model still works'''

        tank = TankFactory.create()
        self.assertNotEqual('', str(tank))

    def test_is_current_hydro(self):
        '''test the currrent_hydro property of the Tank model'''

        tank = TankFactory.create()
        Hydro.objects.create(date=date.today(), tank=tank)
        self.assertEqual(True, tank.is_current_hydro)

    def test_is_current_vip(self):
        '''test the currrent_vip property of the Tank model'''

        tank = TankFactory.create()
        Vip.objects.create(date=date.today(), tank=tank)
        self.assertEqual(True, tank.is_current_vip)

    def test_last_hydro_date(self):
        '''test the last_hydro_date property of the Tank model'''

        tank = TankFactory.create()
        self.assertEqual(None, tank.last_hydro)
        one_year = relativedelta(years=1)
        Hydro.objects.create(date=date.today() - one_year, tank=tank)
        Hydro.objects.create(date=date.today(), tank=tank)
        self.assertNotEqual(None, tank.last_hydro)
        self.assertEqual(date.today(), tank.last_hydro.date)

    def test_last_vip_date(self):
        '''test the last_vip_date property of the Tank model'''

        tank = TankFactory.create()
        self.assertEqual(None, tank.last_vip)
        one_year = relativedelta(years=1)
        Vip.objects.create(date=date.today() - one_year, tank=tank)
        Vip.objects.create(date=date.today(), tank=tank)
        self.assertNotEqual(None, tank.last_vip)
        self.assertEqual(date.today(), tank.last_vip.date)

    def test_clean_good(self):
        '''
            test that the clean method for the Tank model still works
            and that we can have two tanks with the same doubles_code
        '''
        member = MemberFactory.create()
        spec = SpecFactory.create()
        Tank.objects.create(
            owner=member,
            code='test_validate_doubles_code_good_1',
            doubles_code='test_validate_doubles_code_good',
            serial_number='test_validate_doubles_code_good_1',
            spec=spec,
        )
        tank = Tank.objects.create(
            owner=member,
            code='test_validate_doubles_code_good_2',
            doubles_code='test_validate_doubles_code_good',
            serial_number='test_validate_doubles_code_good_2',
            spec=spec,
        )
        self.assertEqual(None, tank.full_clean())

    def test_clean_bad(self):
        '''
            test that the clean method for the Tank model still works
            and that we cannot have three tanks with the same doubles_code
        '''

        with self.assertRaises(ValidationError):
            member = MemberFactory.create()
            spec = SpecFactory.create()
            Tank.objects.create(
                owner=member,
                code='test_validate_doubles_code_bad_1',
                doubles_code='test_validate_doubles_code_bad',
                serial_number='test_validate_doubles_code_bad_1',
                spec=spec,
            )
            Tank.objects.create(
                owner=member,
                code='test_validate_doubles_code_bad_2',
                doubles_code='test_validate_doubles_code_bad',
                serial_number='test_validate_doubles_code_bad_2',
                spec=spec,
            )
            Tank.objects.create(
                owner=member,
                code='test_validate_doubles_code_bad_3',
                doubles_code='test_validate_doubles_code_bad',
                serial_number='test_validate_doubles_code_bad_3',
                spec=spec,
            ).full_clean()

    def test_tank_factor(self):
        '''the tank factor is the number of cubic feet per 100 psi'''

        tank = TankFactory.create()
        self.assertEqual(tank.spec.tank_factor, tank.tank_factor)


class TestHydroModel(TestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    def test_hydro_string(self):
        '''test that the stringify method for the Hydro model still works'''

        tank = TankFactory.create()
        hydro = Hydro.objects.create(tank=tank, date=date.today())
        self.assertNotEqual('', str(hydro))

    def test_current_hydro(self):
        '''test the current method of HydroManager'''

        tank = TankFactory.create()
        count = Hydro.objects.current().count()
        Hydro.objects.create(tank=tank, date=date.today())
        Hydro.objects.create(
            tank=tank,
            date=date.today() - relativedelta(years=10)
        )
        self.assertEqual(count + 1, Hydro.objects.current().count())


class TestVipModel(TestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    def test_vip_string(self):
        '''test that the stringify method for the Vip model still works'''

        tank = TankFactory.create()
        vip = Vip.objects.create(tank=tank, date=date.today())
        self.assertNotEqual('', str(vip))

    def test_current_vip(self):
        '''test the current method of VipManager'''

        tank = TankFactory.create()
        count = Vip.objects.current().count()
        Vip.objects.create(tank=tank, date=date.today())
        Vip.objects.create(
            tank=tank,
            date=date.today() - relativedelta(years=10)
        )
        self.assertEqual(count + 1, Vip.objects.current().count())
