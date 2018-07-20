'''Copyright 2016 DDNY. All Rights Reserved.'''

from datetime import date
from decimal import Decimal
from pytz import timezone

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.messages.constants import WARNING
from django.db.models import Sum

from ddny.core import cash
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
    '''test fillstation views'''

    @test_consent_required(path=reverse("fillstation:blend"))
    @test_login_required(path=reverse("fillstation:blend"))
    def test_blend(self):
        '''test the blend FBV'''
        self.login()
        tank = TankFactory(doubles_code="test_blend")
        Hydro.objects.create(date=date.today(), tank=tank)
        Vip.objects.create(date=date.today(), tank=tank)
        response = self.client.get(reverse("fillstation:blend"))
        self.assertTemplateUsed(response, "fillstation/blend.html")

    @test_consent_required(path=reverse("fillstation:fill"))
    @test_login_required(path=reverse("fillstation:fill"))
    def test_fill(self):
        '''test the fill FBV'''
        self.login()
        tank1 = TankFactory(doubles_code="test_fill1")
        tank2 = TankFactory(code="test_fill2", doubles_code="")
        Hydro.objects.create(date=date.today(), tank=tank1)
        Vip.objects.create(date=date.today(), tank=tank2)
        response = self.client.get(reverse("fillstation:fill"))
        self.assertTemplateUsed(response, "fillstation/fill.html")

    @test_consent_required(path=reverse("fillstation:log"))
    @test_login_required(path=reverse("fillstation:log"))
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
        response = self.client.get(reverse("fillstation:log"))
        self.assertTemplateUsed(response, "fillstation/log.html")

        for f in fills:
            local_datetime = f.datetime.astimezone(timezone(settings.TIME_ZONE))
            self.assertContains(response, f.id)
            self.assertContains(response, f.is_paid)
            self.assertContains(
                response,
                local_datetime.strftime("%Y-%m-%d %H:%M")
            )
            self.assertContains(response, f.blender)
            self.assertContains(response, f.bill_to)
            self.assertContains(response, f.tank_code)
            self.assertContains(response, f.gas_name)
            self.assertContains(response, f.psi_start)
            self.assertContains(response, f.psi_end)
            self.assertContains(response, f.total_price)

    @test_consent_required(path=reverse("fillstation:pay_fills",
                                        kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("fillstation:pay_fills",
                                      kwargs={"slug": "test_login_required"}))
    def test_pay_fills(self):
        '''test the PayFills CBV'''
        self.login()
        gas = GasFactory.create()
        tank1 = TankFactory.create(code="test_pay_1")
        tank2 = TankFactory.create(code="test_pay_2")
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
                viewname="fillstation:pay_fills",
                kwargs={"slug": self.member.slug,},
            )
        )
        self.assertTemplateUsed(response, "fillstation/pay_fills.html")
        self.assertContains(response, gas.name, count=count + 6)
        self.assertContains(response, tank1.code, count=count + 3)
        self.assertContains(response, tank2.code, count=count + 3)
        self.assertNotContains(response, "id_bill_to")
        messages = list(response.context['messages'])
        self.assertEquals(1, len(messages))
        self.assertEqual(WARNING, messages[0].level)

    @test_consent_required(path=reverse("fillstation:prepay"))
    @test_login_required(path=reverse("fillstation:prepay"))
    def test_prepay(self):
        '''test the prepay FBV'''
        self.login()
        response = self.client.get(reverse("fillstation:prepay"))
        self.assertContains(
            response,
            "Prepay"
        )
        self.assertTemplateUsed(response, "fillstation/prepay.html")

    @test_consent_required(path=reverse("fillstation:pay_fills",
                                        kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("fillstation:pay_fills",
                                      kwargs={"slug": "test_login_required"}))
    def test_pay_fills_permission(self):
        '''test the members cannot load the pay_fills page for other members'''
        self.login()
        user = RandomUserFactory.create(username="test_pay_fills_permission")
        random_member = MemberFactory.create(user=user)
        response = self.client.get(
            path=reverse(
                viewname="fillstation:pay_fills",
                kwargs={"slug": random_member.slug}
            )
        )
        self.assertEquals(403, response.status_code)

    @test_login_required(path=reverse("fillstation:pay_fills",
                                      kwargs={"slug": "test_login_required"}))
    def test_pay_fills_fillstation(self):
        '''test the pay fills view'''
        self.client.logout()
        RandomUserFactory.create(username="fillstation", password=make_password("accessdenied"))
        self.assertTrue(
            self.client.login(username="fillstation", password="accessdenied")
        )
        response = self.client.get(
            path=reverse(
                viewname="fillstation:pay_fills",
                kwargs={"slug": "fillstation"}
            )
        )
        self.assertTemplateUsed(response, "fillstation/pay_fills.html")
        self.assertContains(response, "id_bill_to")
        for m in Member.objects.all():
            self.assertContains(response, m.first_name)

    @test_consent_required(path=reverse("fillstation:download"))
    @test_login_required(path=reverse("fillstation:download"))
    def test_download(self):
        '''test the download FBV'''
        self.login()
        response = self.client.get(reverse("fillstation:download"))
        self.assertEquals(
            response.get("Content-Disposition"),
            "attachment; filename='fill_log.csv'"
        )

    @test_consent_required(path=reverse("fillstation:log_fill"))
    @test_login_required(path=reverse("fillstation:log_fill"))
    def test_log_fill_no_hydrovip(self):
        '''test that the log_fill view works'''
        self.login()
        count = Fill.objects.count()
        gas = GasFactory.create()
        tank = TankFactory.create(owner=self.member)
        gas_price = tank.tank_factor * gas.cost
        total_price = cash(gas_price)
        equipment_surcharge = cash(
            float(settings.EQUIPMENT_COST_FIXED) + tank.tank_factor * float(settings.EQUIPMENT_COST_PROPORTIONAL)
        )
        form = {
            "num_rows": 2,
            "blender_0": self.member.username,
            "bill_to_0": self.member.username,
            "tank_code_0": tank.code,
            "gas_name_0": gas.name,
            "psi_start_0": 0,
            "psi_end_0": 100,
            "is_equipment_surcharge_0": False,
            "total_price_0": total_price,
            "is_blend_0": False,
            "blender_1": self.member.username,
            "bill_to_1": self.member.username,
            "tank_code_1": tank.code,
            "gas_name_1": "Equipment",
            "psi_start_1": 0,
            "psi_end_1": 100,
            "is_equipment_surcharge_1": True,
            "total_price_1": equipment_surcharge,
            "is_blend_1": False,
        }
        response = self.client.post(reverse("fillstation:log_fill"), form)
        self.assertTemplateUsed(response, "fillstation/fill_success.html")
        self.assertContains(response, "Thank you")
        self.assertEquals(count + 2, Fill.objects.count())
        self.assertEquals(1, len(mail.outbox))
        self.assertEqual(mail.outbox[0].subject, "DDNY automated warning: hydro/vip")

    @test_consent_required(path=reverse("fillstation:log_fill"))
    @test_login_required(path=reverse("fillstation:log_fill"))
    def test_log_fill_no_prepay(self):
        '''test that the log_fill view works'''
        member = MemberFactory.create()
        self.consent = ConsentAFactory.create(member=member)
        self.client.logout()
        self.assertTrue(self.client.login(
            username=member.user.username,
            password="password"
        ))
        tank = TankFactory.create(owner=member)
        gas = GasFactory.create()
        gas_price = tank.tank_factor * gas.cost
        total_price = cash(gas_price)
        equipment_surcharge = cash(
            float(settings.EQUIPMENT_COST_FIXED) + 2* tank.tank_factor * float(settings.EQUIPMENT_COST_PROPORTIONAL)
        )
        form = {
            "num_rows": 3,
            "blender_0": member.username,
            "bill_to_0": member.username,
            "tank_code_0": tank.code,
            "gas_name_0": gas.name,
            "psi_start_0": 0,
            "psi_end_0": 100,
            "is_equipment_surcharge_0": False,
            "total_price_0": total_price,
            "is_blend_0": False,
            "blender_1": member.username,
            "bill_to_1": member.username,
            "tank_code_1": tank.code,
            "gas_name_1": gas.name,
            "psi_start_1": 0,
            "psi_end_1": 100,
            "is_equipment_surcharge_1": False,
            "total_price_1": total_price,
            "is_blend_1": False,
            "blender_2": member.username,
            "bill_to_2": member.username,
            "tank_code_2": tank.code,
            "gas_name_2": "Equipment",
            "psi_start_2": 0,
            "psi_end_2": 200,
            "is_equipment_surcharge_2": True,
            "total_price_2": equipment_surcharge,
            "is_blend_2": False,
        }
        response = self.client.post(reverse("fillstation:log_fill"), form)

        self.assertTemplateUsed(response, "fillstation/fill_success.html")

        prepaid = Prepay.objects.filter(member=member)
        total_prepaid = prepaid.aggregate(Sum("amount")).get("amount__sum")
        if total_prepaid is None:
            total_prepaid = Decimal(0.0).quantize(settings.PENNY)

        self.assertEquals(Decimal(0.0).quantize(settings.PENNY), total_prepaid)
        self.assertEquals(0, Fill.objects.paid().filter(bill_to=member).count())
        self.assertEquals(3, Fill.objects.unpaid().filter(bill_to=member).count())


    @test_consent_required(path=reverse("fillstation:log_fill"))
    @test_login_required(path=reverse("fillstation:log_fill"))
    def test_log_fill_some_prepay(self):
        '''test that the log_fill view works'''
        member = MemberFactory.create()
        self.consent = ConsentAFactory.create(member=member)
        self.client.logout()
        self.assertTrue(self.client.login(
            username=member.user.username,
            password="password"
        ))

        tank = TankFactory.create(owner=member)
        gas = GasFactory.create()
        gas_price = tank.tank_factor * gas.cost
        total_price = cash(gas_price)
        amount = total_price
        Prepay.objects.create(member=member, amount=amount)
        equipment_surcharge = cash(
            float(settings.EQUIPMENT_COST_FIXED) + 2 * tank.tank_factor * float(settings.EQUIPMENT_COST_PROPORTIONAL)
        )
        form = {
            "num_rows": 3,
            "blender_0": member.username,
            "bill_to_0": member.username,
            "tank_code_0": tank.code,
            "gas_name_0": gas.name,
            "psi_start_0": 0,
            "psi_end_0": 100,
            "is_equipment_surcharge_0": False,
            "total_price_0": total_price,
            "is_blend_0": False,
            "blender_1": member.username,
            "bill_to_1": member.username,
            "tank_code_1": tank.code,
            "gas_name_1": gas.name,
            "psi_start_1": 0,
            "psi_end_1": 100,
            "is_equipment_surcharge_1": False,
            "total_price_1": total_price,
            "is_blend_1": False,
            "blender_2": member.username,
            "bill_to_2": member.username,
            "tank_code_2": tank.code,
            "gas_name_2": "Equipment",
            "psi_start_2": 0,
            "psi_end_2": 200,
            "is_equipment_surcharge_2": True,
            "total_price_2": equipment_surcharge,
            "is_blend_2": False,
        }
        response = self.client.post(reverse("fillstation:log_fill"), form)

        self.assertTemplateUsed(response, "fillstation/fill_success.html")

        prepaid = Prepay.objects.filter(member=member)
        total_prepaid = prepaid.aggregate(Sum("amount")).get("amount__sum")
        if total_prepaid is None:
            total_prepaid = Decimal(0.0).quantize(settings.PENNY)

        self.assertEquals(Decimal(0.0).quantize(settings.PENNY), total_prepaid)
        self.assertEquals(1, Fill.objects.paid().filter(bill_to=member).count())
        self.assertEquals(2, Fill.objects.unpaid().filter(bill_to=member).count())


    @test_consent_required(path=reverse("fillstation:log_fill"))
    @test_login_required(path=reverse("fillstation:log_fill"))
    def test_log_fill_enough_prepay(self):
        '''test that the log_fill view works'''
        member = MemberFactory.create()
        self.consent = ConsentAFactory.create(member=member)
        self.client.logout()
        self.assertTrue(self.client.login(
            username=member.user.username,
            password="password"
        ))

        tank = TankFactory.create(owner=member)
        gas = GasFactory.create()

        cubic_feet = tank.tank_factor
        air_price = \
            cubic_feet * gas.air_fraction * float(settings.AIR_COST)
        argon_price = \
            cubic_feet * gas.argon_fraction * float(settings.ARGON_COST)
        helium_price = \
            cubic_feet * gas.helium_fraction * float(settings.HELIUM_COST)
        oxygen_price = \
            cubic_feet * gas.oxygen_fraction * float(settings.OXYGEN_COST)
        other_price = \
            cubic_feet * gas.other_fraction * float(settings.OTHER_COST)
        gas_price = \
            air_price + argon_price + helium_price + oxygen_price + other_price
        gas_price = cash(gas_price)

        equipment_surcharge = cash(
            float(settings.EQUIPMENT_COST_FIXED) + 2 * tank.tank_factor * float(settings.EQUIPMENT_COST_PROPORTIONAL)
        )
        total_price = 2 * gas_price + equipment_surcharge
        amount = total_price + cash(0.5)
        Prepay.objects.create(member=member, amount=amount)
        form = {
            "num_rows": 3,
            "blender_0": member.username,
            "bill_to_0": member.username,
            "tank_code_0": tank.code,
            "gas_name_0": gas.name,
            "psi_start_0": 0,
            "psi_end_0": 100,
            "is_equipment_surcharge_0": False,
            "total_price_0": gas_price,
            "is_blend_0": False,
            "blender_1": member.username,
            "bill_to_1": member.username,
            "tank_code_1": tank.code,
            "gas_name_1": gas.name,
            "psi_start_1": 0,
            "psi_end_1": 100,
            "is_equipment_surcharge_1": False,
            "total_price_1": gas_price,
            "is_blend_1": False,
            "blender_2": member.username,
            "bill_to_2": member.username,
            "tank_code_2": tank.code,
            "gas_name_2": "Equipment",
            "psi_start_2": 0,
            "psi_end_2": 200,
            "is_equipment_surcharge_2": True,
            "total_price_2": equipment_surcharge,
            "is_blend_2": False,
        }
        response = self.client.post(reverse("fillstation:log_fill"), form)

        self.assertTemplateUsed(response, "fillstation/fill_success.html")

        prepaid = Prepay.objects.filter(member=member)
        total_prepaid = prepaid.aggregate(Sum("amount")).get("amount__sum")
        if total_prepaid is None:
            total_prepaid = Decimal(0.0).quantize(settings.PENNY)

        self.assertEquals(Decimal(0.5).quantize(settings.PENNY), total_prepaid)
        self.assertEquals(3, Fill.objects.paid().filter(bill_to=member).count())
        self.assertEquals(0, Fill.objects.unpaid().filter(bill_to=member).count())


    @test_consent_required(path=reverse("fillstation:log_fill"))
    @test_login_required(path=reverse("fillstation:log_fill"))
    def test_log_fill_suspicious_operation(self):
        '''test that the log_fill view catches suspicious operations'''
        self.login()
        gas = GasFactory.create()
        tank = TankFactory.create(owner=self.member)
        equipment_surcharge = cash(
            float(settings.EQUIPMENT_COST_FIXED) + 31 * tank.tank_factor * float(settings.EQUIPMENT_COST_PROPORTIONAL)
        )
        form = {
            "num_rows": 3,
            "blender_0": self.member.username,
            "bill_to_0": self.member.username,
            "tank_code_0": tank.code,
            "gas_name_0": gas.name,
            "psi_start_0": 0,
            "psi_end_0": 3000,
            "is_equipment_surcharge_0": False,
            "total_price_0": 10.00,
            "is_blend_0": False,
            "blender_1": self.member.username,
            "bill_to_1": self.member.username,
            "tank_code_1": tank.code,
            "gas_name_1": gas.name,
            "psi_start_1": 0,
            "psi_end_1": 100,
            "is_equipment_surcharge_1": True,
            "total_price_2": equipment_surcharge,
            "blender_2": self.member.username,
            "bill_to_2": self.member.username,
            "tank_code_2": tank.code,
            "gas_name_2": "Equipment",
            "psi_start_2": 0,
            "psi_end_2": 3100,
            "is_equipment_surcharge_2": True,
            "total_price_3": equipment_surcharge,
            "is_blend_3": False,
        }
        response = self.client.post(reverse("fillstation:log_fill"), form)
        self.assertTemplateUsed(response, "ddny/oops.html")
        self.assertContains(response, "Oops!")
        self.assertContains(response, "Price verification failure.")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "DDNY automated warning: log_fill")
