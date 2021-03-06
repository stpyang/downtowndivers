'''Copyright 2016 DDNY. All Rights Reserved.'''

from datetime import date
from decimal import Decimal
from pytz import timezone

from django.conf import settings
from django.core import mail
from django.contrib.auth.hashers import make_password
from django.contrib.messages.constants import WARNING
from django.db.models import Sum
from django.urls import reverse

from ddny.core import cash
from ddny.settings import costs
from ddny.test_decorators import test_consent_required, test_login_required
from ddny.test_views import BaseDdnyTestCase
from gas.factory import GasFactory
from registration.factory import ConsentAFactory, MemberFactory, RandomUserFactory
from registration.models import Member
from tank.factory import TankFactory
from tank.models import Hydro, Vip
from .factory import FillFactory
from .models import Fill, Prepay


class TestFillstationViews(BaseDdnyTestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    @test_consent_required(path=reverse('fillstation:blend'))
    @test_login_required(path=reverse('fillstation:blend'))
    def test_blend(self):
        '''test the blend FBV'''

        self.login()
        tank = TankFactory(doubles_code='test_blend')
        Hydro.objects.create(date=date.today(), tank=tank)
        Vip.objects.create(date=date.today(), tank=tank)
        response = self.client.get(reverse('fillstation:blend'))
        self.assertTemplateUsed(response, 'fillstation/blend.html')

    @test_consent_required(path=reverse('fillstation:fill'))
    @test_login_required(path=reverse('fillstation:fill'))
    def test_fill(self):
        '''test the fill FBV'''

        self.login()
        tank1 = TankFactory(doubles_code='test_fill1')
        tank2 = TankFactory(code='test_fill2', doubles_code='')
        Hydro.objects.create(date=date.today(), tank=tank1)
        Vip.objects.create(date=date.today(), tank=tank2)
        response = self.client.get(reverse('fillstation:fill'))
        self.assertTemplateUsed(response, 'fillstation/fill.html')

    @test_consent_required(path=reverse('fillstation:log'))
    @test_login_required(path=reverse('fillstation:log'))
    def test_log(self):
        '''test the Log CBV'''

        self.login()
        fills = FillFactory.create_batch(
            10,
            user=self.user,
            blender=self.member,
            bill_to=self.member,
            is_paid=True,
        )
        response = self.client.get(reverse('fillstation:log'))
        self.assertTemplateUsed(response, 'fillstation/log.html')

        for fill in fills:
            local_datetime = fill.datetime.astimezone(timezone(settings.TIME_ZONE))
            self.assertContains(response, fill.id)
            self.assertContains(response, fill.is_paid)
            self.assertContains(
                response,
                local_datetime.strftime('%Y-%m-%d %H:%M')
            )
            self.assertContains(response, fill.blender)
            self.assertContains(response, fill.bill_to)
            self.assertContains(response, fill.tank_code)
            self.assertContains(response, fill.gas_name)
            self.assertContains(response, fill.psi_start)
            self.assertContains(response, fill.psi_end)
            self.assertContains(response, fill.total_price)

    @test_login_required(
        path=reverse('fillstation:pay_fills', kwargs={'slug': 'test_login_required'})
    )
    def test_pay_fills(self):
        '''test the PayFills CBV'''

        self.login()
        gas = GasFactory.create()
        tank1 = TankFactory.create(code='test_pay_1')
        tank2 = TankFactory.create(code='test_pay_2')
        Hydro.objects.create(date=date.today(), tank=tank1)
        Vip.objects.create(date=date.today(), tank=tank2)
        count = Fill.objects.unpaid().filter(user=self.user).count()
        FillFactory.create_batch(
            3,
            user=self.user,
            blender=self.member,
            bill_to=self.member,
            gas_name=gas.name,
            gas_slug=gas.slug,
            tank_code=tank1.code,
            is_paid=True,
        )
        FillFactory.create_batch(
            3,
            user=self.user,
            blender=self.member,
            bill_to=self.member,
            gas_name=gas.name,
            gas_slug=gas.slug,
            tank_code=tank1.code,
            is_paid=False,
        )
        FillFactory.create_batch(
            3,
            user=self.user,
            blender=self.member,
            bill_to=self.member,
            gas_name=gas.name,
            gas_slug=gas.slug,
            tank_code=tank2.code,
            is_paid=False,
        )
        response = self.client.get(
            reverse(
                viewname='fillstation:pay_fills',
                kwargs={'slug': self.member.slug, },
            )
        )
        self.assertTemplateUsed(response, 'fillstation/pay_fills.html')
        self.assertContains(response, gas.get_absolute_url(), count=count + 6)
        self.assertContains(response, tank1.get_absolute_url(), count=count + 3)
        self.assertContains(response, tank2.get_absolute_url(), count=count + 3)
        self.assertNotContains(response, 'id_bill_to')
        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertEqual(WARNING, messages[0].level)

    @test_consent_required(path=reverse('fillstation:prepay'))
    @test_login_required(path=reverse('fillstation:prepay'))
    def test_prepay(self):
        '''test the prepay FBV'''

        self.login()
        response = self.client.get(reverse('fillstation:prepay'))
        self.assertContains(
            response,
            'Prepay'
        )
        self.assertTemplateUsed(response, 'fillstation/prepay.html')

    @test_login_required(
        path=reverse('fillstation:pay_fills', kwargs={'slug': 'test_login_required'})
    )
    def test_pay_fills_permission(self):
        '''test the members cannot load the pay_fills page for other members'''

        self.login()
        user = RandomUserFactory.create(username='test_pay_fills_permission')
        random_member = MemberFactory.create(user=user)
        response = self.client.get(
            path=reverse(
                viewname='fillstation:pay_fills',
                kwargs={'slug': random_member.slug}
            )
        )
        self.assertEqual(403, response.status_code)

    @test_login_required(
        path=reverse('fillstation:pay_fills', kwargs={'slug': 'test_login_required'})
    )
    def test_pay_fills_fillstation(self):
        '''test the pay fills view'''

        self.client.logout()
        RandomUserFactory.create(username='fillstation', password=make_password('accessdenied'))
        self.assertTrue(
            self.client.login(username='fillstation', password='accessdenied')
        )
        response = self.client.get(
            path=reverse(
                viewname='fillstation:pay_fills',
                kwargs={'slug': 'fillstation'}
            )
        )
        self.assertTemplateUsed(response, 'fillstation/pay_fills.html')
        self.assertContains(response, 'id_bill_to')
        for member in Member.objects.all():
            self.assertContains(response, member.first_name)

    @test_consent_required(path=reverse('fillstation:download'))
    @test_login_required(path=reverse('fillstation:download'))
    def test_download(self):

        '''test the download FBV'''
        self.login()
        response = self.client.get(reverse('fillstation:download'))
        self.assertEqual(
            response.get('Content-Disposition'),
            'attachment; filename=ddny_fill_log'
        )

    @test_consent_required(path=reverse('fillstation:log_fill'))
    @test_login_required(path=reverse('fillstation:log_fill'))
    def test_log_fill_no_hydrovip(self):
        '''test that the log_fill view works'''

        self.login()
        count = Fill.objects.count()
        gas = GasFactory.create()
        tank = TankFactory.create(owner=self.member)
        total_price = tank.tank_factor * (gas.cost + float(costs.EQUIPMENT_COST_PROPORTIONAL))
        form = {
            'num_rows': 2,
            'blender_0': self.member.username,
            'bill_to_0': self.member.username,
            'tank_code_0': tank.code,
            'gas_name_0': gas.name,
            'psi_start_0': 0,
            'psi_end_0': 100,
            'is_equipment_surcharge_0': False,
            'total_price_0': cash(total_price),
            'is_blend_0': False,
            'blender_1': self.member.username,
            'bill_to_1': self.member.username,
            'tank_code_1': tank.code,
            'is_equipment_surcharge_1': True,
            'total_price_1': costs.EQUIPMENT_COST_FIXED,
            'is_blend_1': False,
        }
        response = self.client.post(reverse('fillstation:log_fill'), form)
        self.assertTemplateUsed(response, 'fillstation/fill_success.html')
        self.assertContains(response, 'Thank you')
        self.assertEqual(count + 2, Fill.objects.count())
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(mail.outbox[0].subject, 'DDNY automated warning: hydro/vip')

    @test_consent_required(path=reverse('fillstation:log_fill'))
    @test_login_required(path=reverse('fillstation:log_fill'))
    def test_log_fill_no_prepay(self):
        '''test that the log_fill view works'''

        member = MemberFactory.create()
        self.consent = ConsentAFactory.create(member=member)
        self.client.logout()
        self.assertTrue(self.client.login(
            username=member.user.username,
            password='password'
        ))
        tank = TankFactory.create(owner=member)
        gas = GasFactory.create()
        total_price = cash(tank.tank_factor * (
            gas.cost + float(costs.EQUIPMENT_COST_PROPORTIONAL)
        ))
        form = {
            'num_rows': 3,
            'blender_0': member.username,
            'bill_to_0': member.username,
            'tank_code_0': tank.code,
            'gas_name_0': gas.name,
            'psi_start_0': 0,
            'psi_end_0': 100,
            'is_equipment_surcharge_0': False,
            'total_price_0': total_price,
            'is_blend_0': False,
            'blender_1': member.username,
            'bill_to_1': member.username,
            'tank_code_1': tank.code,
            'gas_name_1': gas.name,
            'psi_start_1': 0,
            'psi_end_1': 100,
            'is_equipment_surcharge_1': False,
            'total_price_1': total_price,
            'is_blend_1': False,
            'blender_2': member.username,
            'bill_to_2': member.username,
            'tank_code_2': tank.code,
            'is_equipment_surcharge_2': True,
            'total_price_2': costs.EQUIPMENT_COST_FIXED,
            'is_blend_2': False,
        }
        response = self.client.post(reverse('fillstation:log_fill'), form)

        self.assertTemplateUsed(response, 'fillstation/fill_success.html')

        prepaid = Prepay.objects.filter(member=member)
        total_prepaid = prepaid.aggregate(Sum('amount')).get('amount__sum')
        if total_prepaid is None:
            total_prepaid = Decimal(0.0).quantize(costs.PENNY)

        self.assertEqual(Decimal(0.0).quantize(costs.PENNY), total_prepaid)
        self.assertEqual(0, Fill.objects.paid().filter(bill_to=member).count())
        self.assertEqual(3, Fill.objects.unpaid().filter(bill_to=member).count())

    @test_consent_required(path=reverse('fillstation:log_fill'))
    @test_login_required(path=reverse('fillstation:log_fill'))
    def test_log_fill_some_prepay(self):
        '''test that the log_fill view works'''

        member = MemberFactory.create()
        self.consent = ConsentAFactory.create(member=member)
        self.client.logout()
        self.assertTrue(self.client.login(
            username=member.user.username,
            password='password'
        ))

        tank = TankFactory.create(owner=member)
        gas = GasFactory.create()
        total_price = tank.tank_factor * (gas.cost + float(costs.EQUIPMENT_COST_PROPORTIONAL))
        prepay_amount = cash(total_price)
        Prepay.objects.create(member=member, amount=prepay_amount)
        form = {
            'num_rows': 3,
            'blender_0': member.username,
            'bill_to_0': member.username,
            'tank_code_0': tank.code,
            'gas_name_0': gas.name,
            'psi_start_0': 0,
            'psi_end_0': 100,
            'is_equipment_surcharge_0': False,
            'total_price_0': cash(total_price),
            'is_blend_0': False,
            'blender_1': member.username,
            'bill_to_1': member.username,
            'tank_code_1': tank.code,
            'gas_name_1': gas.name,
            'psi_start_1': 0,
            'psi_end_1': 100,
            'is_equipment_surcharge_1': False,
            'total_price_1': total_price,
            'is_blend_1': False,
            'blender_2': member.username,
            'bill_to_2': member.username,
            'tank_code_2': tank.code,
            'is_equipment_surcharge_2': True,
            'total_price_2': costs.EQUIPMENT_COST_FIXED,
            'is_blend_2': False,
        }
        response = self.client.post(reverse('fillstation:log_fill'), form)

        self.assertTemplateUsed(response, 'fillstation/fill_success.html')

        prepaid = Prepay.objects.filter(member=member)
        total_prepaid = prepaid.aggregate(Sum('amount')).get('amount__sum')
        if total_prepaid is None:
            total_prepaid = Decimal(0.0).quantize(costs.PENNY)

        self.assertEqual(Decimal(0.0).quantize(costs.PENNY), total_prepaid)
        self.assertEqual(1, Fill.objects.paid().filter(bill_to=member).count())
        self.assertEqual(2, Fill.objects.unpaid().filter(bill_to=member).count())

    @test_consent_required(path=reverse('fillstation:log_fill'))
    @test_login_required(path=reverse('fillstation:log_fill'))
    def test_log_fill_enough_prepay(self):
        '''test that the log_fill view works'''

        member = MemberFactory.create()
        self.consent = ConsentAFactory.create(member=member)
        self.client.logout()
        self.assertTrue(self.client.login(
            username=member.user.username,
            password='password'
        ))

        tank = TankFactory.create(owner=member)
        gas = GasFactory.create()

        cubic_feet = tank.tank_factor
        gas_price = cubic_feet * gas.cost
        equipment_price = cubic_feet * float(costs.EQUIPMENT_COST_PROPORTIONAL)
        total_price = gas_price + equipment_price

        prepay_amount = 2 * cash(total_price) + cash(costs.EQUIPMENT_COST_FIXED) + cash(1.0)
        Prepay.objects.create(member=member, amount=prepay_amount)
        form = {
            'num_rows': 3,
            'blender_0': member.username,
            'bill_to_0': member.username,
            'tank_code_0': tank.code,
            'gas_name_0': gas.name,
            'psi_start_0': 0,
            'psi_end_0': 100,
            'is_equipment_surcharge_0': False,
            'total_price_0': cash(total_price),
            'is_blend_0': False,
            'blender_1': member.username,
            'bill_to_1': member.username,
            'tank_code_1': tank.code,
            'gas_name_1': gas.name,
            'psi_start_1': 0,
            'psi_end_1': 100,
            'is_equipment_surcharge_1': False,
            'total_price_1': cash(total_price),
            'is_blend_1': False,
            'blender_2': member.username,
            'bill_to_2': member.username,
            'tank_code_2': tank.code,
            'is_equipment_surcharge_2': True,
            'total_price_2': costs.EQUIPMENT_COST_FIXED,
            'is_blend_2': False,
        }
        response = self.client.post(reverse('fillstation:log_fill'), form)
        self.assertTemplateUsed(response, 'fillstation/fill_success.html')

        prepaid = Prepay.objects.filter(member=member)
        total_prepaid = prepaid.aggregate(Sum('amount')).get('amount__sum')
        if total_prepaid is None:
            total_prepaid = cash(0)

        self.assertEqual(cash(1.0), total_prepaid)
        self.assertEqual(3, Fill.objects.paid().filter(bill_to=member).count())
        self.assertEqual(0, Fill.objects.unpaid().filter(bill_to=member).count())

    @test_consent_required(path=reverse('fillstation:log_fill'))
    @test_login_required(path=reverse('fillstation:log_fill'))
    def test_log_fill_suspicious_operation(self):
        '''test that the log_fill view catches suspicious operations'''

        self.login()
        gas = GasFactory.create()
        tank = TankFactory.create(owner=self.member)
        form = {
            'num_rows': 3,
            'blender_0': self.member.username,
            'bill_to_0': self.member.username,
            'tank_code_0': tank.code,
            'gas_name_0': gas.name,
            'psi_start_0': 0,
            'psi_end_0': 3000,
            'is_equipment_surcharge_0': False,
            'total_price_0': 10.00,
            'is_blend_0': False,
            'blender_1': self.member.username,
            'bill_to_1': self.member.username,
            'tank_code_1': tank.code,
            'is_equipment_surcharge_1': True,
            'total_price_1': costs.EQUIPMENT_COST_FIXED,
            'blender_2': self.member.username,
            'bill_to_2': self.member.username,
            'tank_code_2': tank.code,
            'is_equipment_surcharge_2': True,
            'total_price_2': costs.EQUIPMENT_COST_FIXED,
            'is_blend_2': False,
        }
        response = self.client.post(reverse('fillstation:log_fill'), form)
        self.assertTemplateUsed(response, 'ddny/oops.html')
        self.assertContains(response, 'Oops!')
        self.assertContains(response, 'verification failure.')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'DDNY automated warning: log_fill')
