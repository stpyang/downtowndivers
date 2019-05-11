'''Copyright 2016 DDNY. All Rights Reserved.'''

from datetime import date

from django.contrib.messages.constants import INFO, WARNING
from django.forms.models import modelform_factory
from django.urls import reverse
from django.utils.text import slugify

from ddny.test_decorators import test_login_required
from ddny.test_views import BaseDdnyTestCase
from .factory import SpecFactory, TankFactory, VipFactory
from .models import Hydro, Specification, Tank, Vip


class TestTankViews(BaseDdnyTestCase):
    '''test tank views'''

    def setUp(self):
        super(TestTankViews, self).setUp()
        if not Specification.objects.filter(slug="test_login_required").count():
            SpecFactory.create(name="test_login_required")
        if not Tank.objects.filter(code="test_login_required").count():
            TankFactory.create(code="test_login_required")

    @test_login_required(path=reverse("tank:create"))
    def test_tank_create(self):
        '''test the TankCreate CBV'''
        self.login()
        response = self.client.get(reverse("tank:create"))
        self.assertTemplateUsed(response, "tank/tank_form.html")
        self.assertContains(response, "Create Tank")

    @test_login_required(path=reverse("tank:detail", kwargs={"slug": "test_login_required"}))
    def test_tank_detail(self):
        '''test the TankDetail CBV'''
        self.login()
        tank = TankFactory.create()
        response = self.client.get(tank.get_absolute_url())
        self.assertTemplateUsed(response, "tank/tank_detail.html")
        self.assertContains(response, tank.code)

    @test_login_required(path=reverse("tank:list"))
    def test_tank_list(self):
        '''test the TankList CBV'''
        self.login()
        tanks = TankFactory.create_batch(10)
        response = self.client.get(reverse("tank:list"))
        self.assertTemplateUsed(response, "tank/tank_list.html")
        for tank in tanks:
            self.assertContains(response, tank.code)
            self.assertContains(response, tank.doubles_code)
            self.assertContains(response, tank.spec.name)
            self.assertContains(response, tank.owner.first_name)
            if tank.last_hydro:
                self.assertContains(response, tank.last_hydro.date.strftime("%Y-%m"))
            if tank.last_vip:
                self.assertContains(response, tank.last_vip.date.strftime("%Y-%m"))

    @test_login_required(path=reverse("tank:update", kwargs={"slug": "test_login_required"}))
    def test_tank_update(self):
        '''test the TankUpdate CBV'''
        self.login()
        count = Tank.objects.count()
        response = self.client.get(
            path=reverse(
                viewname="tank:update",
                kwargs={"slug": "test_login_required"}
            )
        )
        self.assertTemplateUsed(response, "tank/tank_form.html")
        self.assertContains(response, "Update test_login_required")
        self.assertEqual(count, Tank.objects.count())

    @test_login_required(path=reverse("tank:create"))
    def test_tank_create_form(self):
        '''test the TankCreate form'''
        self.login()
        count = Tank.objects.count()
        spec = SpecFactory.create()
        tank = TankFactory.build()
        data = {
            "serial_number": tank.serial_number,
            "code": tank.code,
            "owner": self.member.id,
            "spec": spec.id,
            "hydro_set-0-date": "",
            "hydro_set-TOTAL_FORMS": 1,
            "hydro_set-INITIAL_FORMS": 0,
            "hydro_set-MIN_NUM_FORMS": 0,
            "hydro_set-MAX_NUM_FORMS": 1000,
        }
        # TODO(stpyang): fix
        # Form = modelform_factory(Tank, fields=data)
        # self.assertTrue(Form(data).is_valid())
        response = self.client.post(
            path=reverse("tank:create"),
            data=data,
            follow=True,
        )
        self.assertTrue(tank.is_active)
        self.assertEqual(count + 1, Tank.objects.count())
        messages = list(response.context["messages"])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, INFO)

    @test_login_required(path=reverse("tank:create"))
    def test_tank_create_cancel(self):
        '''test the TankCreate cancel'''
        self.login()
        count = Tank.objects.count()
        data = {
            "code": "cancel",
            "cancel": True,
        }
        response = self.client.post(
            path=reverse("tank:create"),
            data=data,
            follow=True,
        )
        self.assertEqual(count, Tank.objects.count())
        self.assertEqual(0, Tank.objects.filter(code="cancel").count())
        self.assertTemplateUsed(response, "tank/tank_list.html")
        messages = list(response.context["messages"])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, WARNING)

    @test_login_required(path=reverse("tank:create"))
    def test_tank_create_form_hydro_inline(self):
        '''test the TankCreate form with HydroInline'''
        self.login()
        tank_count = Tank.objects.count()
        hydro_count = Hydro.objects.count()
        spec = SpecFactory.create()
        tank = TankFactory.build()
        data = {
            "serial_number": tank.serial_number,
            "code": tank.code,
            "owner": self.member.id,
            "spec": spec.id,
            "is_active": tank.is_active,
            "hydro_set-0-date": date.today().strftime("%Y-%m-%d"),
            "hydro_set-TOTAL_FORMS": 1,
            "hydro_set-INITIAL_FORMS": 0,
            "hydro_set-MIN_NUM_FORMS": 0,
            "hydro_set-MAX_NUM_FORMS": 1000,
        }
        # TODO(stpyang): fix
        # Form = modelform_factory(Tank, fields=data)
        # self.assertTrue(Form(data).is_valid())
        response = self.client.post(
            path=reverse("tank:create"),
            data=data,
            follow=True)
        self.assertTrue(tank.is_active)
        self.assertEqual(tank_count + 1, Tank.objects.count())
        self.assertEqual(hydro_count + 1, Hydro.objects.count())
        messages = list(response.context["messages"])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, INFO)

    @test_login_required(path=reverse("tank:update", kwargs={"slug": "test_login_required"}))
    def test_tank_update_form(self):
        '''test the TankUpdate form'''
        self.login()
        tank = TankFactory.create()
        count = Tank.objects.count()
        data = {
            "serial_number": "update",
            "code": "update",
            "owner": self.member.id,
            "spec": tank.spec.id,
            "is_active": tank.is_active,
            "hydro_set-0-date": "",
            "hydro_set-TOTAL_FORMS": 1,
            "hydro_set-INITIAL_FORMS": 0,
            "hydro_set-MIN_NUM_FORMS": 0,
            "hydro_set-MAX_NUM_FORMS": 1000,
        }
        # TODO(stpyang): fix
        # Form = modelform_factory(Tank, fields=data)
        # self.assertTrue(Form(data).is_valid())
        self.assertEqual(0, Tank.objects.filter(code="update").count())
        response = self.client.post(
            path=reverse("tank:update", kwargs={"slug": tank.code}),
            data=data,
            follow=True,
        )
        self.assertEqual(1, Tank.objects.filter(code="update").count())
        tank = Tank.objects.get(code="update")
        self.assertEqual(tank.serial_number, "update")
        self.assertTrue(tank.is_active)
        self.assertEqual(count, Tank.objects.count())
        messages = list(response.context["messages"])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, INFO)

    @test_login_required(path=reverse("tank:update", kwargs={"slug": "test_login_required"}))
    def test_tank_update_cancel(self):
        '''test the TankUpdate cancel'''
        self.login()
        data = {
            "serial_number": "cancel",
            "code": "cancel",
            "cancel": True,
        }
        response = self.client.post(
            path=reverse("tank:update", kwargs={"slug": slugify("test_login_required")}),
            data=data,
            follow=True,
        )
        self.assertEqual(0, Tank.objects.filter(serial_number="cancel").count())
        self.assertEqual(0, Tank.objects.filter(code="cancel").count())
        self.assertTemplateUsed(response, "tank/tank_detail.html")
        messages = list(response.context["messages"])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, WARNING)


class TestSpecViews(BaseDdnyTestCase):
    '''test spec views'''

    def setUp(self):
        super(TestSpecViews, self).setUp()
        if not Specification.objects.filter(name="test_login_required").count():
            SpecFactory.create(name="test_login_required")

    @test_login_required(path=reverse("spec_create"))
    def test_spec_create(self):
        '''test the SpecCreate CBV'''
        self.login()
        count = Specification.objects.count()
        response = self.client.get(reverse("spec_create"))
        self.assertTemplateUsed(response, "tank/spec_form.html")
        self.assertContains(response, "Create Spec")
        self.assertEqual(count, Specification.objects.count())

    @test_login_required(path=reverse("spec_detail", kwargs={"slug": "test_login_required"}))
    def test_spec_detail(self):
        '''test the SpecDetail CBV'''
        self.login()
        spec = SpecFactory.create()
        response = self.client.get(spec.get_absolute_url())
        self.assertTemplateUsed(response, "tank/spec_detail.html")
        self.assertContains(response, spec.name)

    @test_login_required(path=reverse("spec_list"))
    def test_spec_list(self):
        '''test the SpecList CBV'''
        self.login()
        specs = SpecFactory.create_batch(10)
        response = self.client.get(reverse("spec_list"))
        self.assertTemplateUsed(response, "tank/spec_list.html")
        for spec in specs:
            self.assertContains(response, spec.name)
            self.assertContains(response, spec.material)
            self.assertContains(response, "{0:.1f}".format(spec.volume))
            self.assertContains(response, spec.working_pressure)

    @test_login_required(path=reverse("spec_update", kwargs={"slug": "test_login_required"}))
    def test_spec_update(self):
        '''test the SpecUpdate CBV'''
        self.login()
        count = Specification.objects.count()
        response = self.client.get(
            path=reverse(
                viewname="spec_update",
                kwargs={"slug": "test_login_required"},
            )
        )
        self.assertTemplateUsed(response, "tank/spec_form.html")
        self.assertContains(response, "Update test_login_required")
        self.assertEqual(count, Specification.objects.count())

    @test_login_required(path=reverse("spec_create"))
    def test_spec_create_form(self):
        '''test the SpecCreate form'''
        self.login()
        count = Specification.objects.count()
        spec = SpecFactory.build()
        data = {
            "name": spec.name,
            "material": spec.material,
            "volume": spec.volume,
            "working_pressure": spec.working_pressure,
        }
        Form = modelform_factory(Specification, fields=data)
        self.assertTrue(Form(data).is_valid())
        response = self.client.post(
            path=reverse("spec_create"),
            data=data,
            follow=True,
        )
        self.assertEqual(count + 1, Specification.objects.count())
        messages = list(response.context["messages"])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, INFO)

    @test_login_required(path=reverse("spec_create"))
    def test_spec_create_cancel(self):
        '''test the SpecCreate cancel'''
        self.login()
        count = Specification.objects.count()
        data = {
            "name": "cancel",
            "cancel": True,
        }
        response = self.client.post(
            path=reverse("spec_create"),
            data=data,
            follow=True,
        )
        self.assertEqual(count, Specification.objects.count())
        self.assertEqual(0, Specification.objects.filter(name="cancel").count())
        self.assertTemplateUsed(response, "tank/spec_list.html")
        messages = list(response.context["messages"])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, WARNING)

    @test_login_required(path=reverse("spec_update", kwargs={"slug": "test_login_required"}))
    def test_spec_update_form(self):
        '''test the SpecUpdate form'''
        self.login()
        spec = SpecFactory.create()
        data = {
            "name": "update",
            "material": spec.material,
            "volume": spec.volume,
            "working_pressure": spec.working_pressure,
        }
        # Form = modelform_factory(Specification, fields=data)
        # self.assertTrue(Form(data).is_valid())
        self.assertEqual(0, Specification.objects.filter(name="update").count())
        response = self.client.post(
            path=reverse("spec_update", kwargs={"slug": spec.slug}),
            data=data,
            follow=True,
        )
        self.assertEqual(1, Specification.objects.filter(name="update").count())
        messages = list(response.context["messages"])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, INFO)

    @test_login_required(path=reverse("spec_update", kwargs={"slug": "test_login_required"}))
    def test_spec_update_cancel(self):
        '''test the SpecUpdate cancel'''
        self.login()
        data = {
            "name": "cancel",
            "cancel": True,
        }
        response = self.client.post(
            path=reverse(
                viewname="spec_update",
                kwargs={"slug": "test_login_required"},
            ),
            data=data,
            follow=True,
        )
        self.assertEqual(0, Specification.objects.filter(name="cancel").count())
        self.assertTemplateUsed(response, "tank/spec_detail.html")
        messages = list(response.context["messages"])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, WARNING)


class TestVipViews(BaseDdnyTestCase):
    '''test Vip views'''

    def setUp(self):
        super(TestVipViews, self).setUp()
        if not Specification.objects.filter(name="test_login_required").count():
            SpecFactory.create(name="test_login_required")
        if not Tank.objects.filter(code="test_login_required").count():
            TankFactory.create(code="test_login_required")
        if not Vip.objects.filter(id=1).count():
            VipFactory.create()

    @test_login_required(path=reverse("vip_create", kwargs={"slug": "test_login_required"}))
    def test_vip_create(self):
        '''test the VipCreate CBV'''
        self.login()
        response = self.client.get(
            path=reverse(
                viewname="vip_create",
                kwargs={"slug": "test_login_required"},
            )
        )
        self.assertTemplateUsed(response, "tank/vip_form.html")
        self.assertContains(response, "Visual Cylinder Inspection Evaluation Form")

    @test_login_required(path=reverse("vip_detail", kwargs={"pk": 1}))
    def test_tank_detail(self):
        '''test the VipDetail CBV'''
        self.login()
        vip = VipFactory.create()
        response = self.client.get(vip.get_absolute_url())
        self.assertTemplateUsed(response, "tank/vip_detail.html")

    @test_login_required(path=reverse("vip_list"))
    def test_vip_list(self):
        '''test the VipList CBV'''
        self.login()
        vips = VipFactory.create_batch(10)
        response = self.client.get(reverse("vip_list"))
        self.assertTemplateUsed(response, "tank/vip_list.html")
        for vip in vips:
            self.assertContains(response, vip.date.strftime("%Y-%m-%d"))

    @test_login_required(path=reverse("vip_create", kwargs={"slug": "test_login_required"}))
    def test_vip_create_form(self):
        '''test the VipCreate form'''
        self.login()
        count = Vip.objects.count()
        data = {
            "tank": Tank.objects.get(code="test_login_required").id,
            "tank_owners_name": self.member.full_name,
            "date": date.today().strftime("%Y-%m-%d"),
            "address": "",
            "city": "",
            "state": "",
            "zip_code": "12345",
            "phone_number": "123-456-7890",
            "tank_spec_name": "",
            "tank_serial_number": "12345",
            "tank_first_hydro_date": date.today().strftime("%Y-%m-%d"),
            "tank_last_hydro_date": date.today().strftime("%Y-%m-%d"),
            "tank_specification": Specification.objects.get(name="test_login_required"),
            "tank_working_pressure": "3000",
            "tank_material": "Aluminum",
            "external_evidence_of_heat_damage": "No",
            "external_repainting": "No",
            "external_odor": "No",
            "external_bow": "No",
            "external_evidence_of_bulges": "No",
            "external_hammer_tone_test": "No",
            "external_description_of_surface": "",
            "external_line_corrosion": "No",
            "external_comparison_to_psi_standards": "Accept",
            "internal_composition_of_contents": "",
            "internal_description_of_surface": "",
            "internal_pitting": "No",
            "internal_comparison_to_psi_standards": "Accept",
            "threads_description": "",
            "threads_crack_assessment": "",
            "threads_oring_gland_surface": "",
            "threads_eddy_current_test": "No",
            "threads_comparison_to_psi_standards": "Accept",
            "valve_service_needed": "No",
            "valve_burst_disc_replaced": "No",
            "valve_oring_replaced": "No",
            "valve_dip_tube_replaced": "No",
            "valve_threads_checked": "No",
            "valve_thread_condition": "",
            "cylindercondition": "Accept",
            "cylindercondition_sticker_affixed": "No",
            "cylindercondition_sticker_date": date.today().strftime("%Y-%m-%d"),
            "cylindercondition_sticker_notation": "",
            "cylindercondition_clean": False,
            "cylindercondition_tumble": False,
            "cylindercondition_hydro": False,
            "cylindercondition_other": False,
            "cylindercondition_inspector_initials": "",
            "cylindercondition_discard": False,
            "inspector_name": self.member.full_name,
            "inspector_psi_number": 0,
        }
        Form = modelform_factory(Vip, fields=data)
        self.assertTrue(Form(data).is_valid())
        response = self.client.post(
            path=reverse(
                viewname="vip_create",
                kwargs={"slug": "test_login_required"}
            ),
            data=data,
            follow=True,
        )
        self.assertEqual(count + 1, Vip.objects.count())
        messages = list(response.context["messages"])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, INFO)


    @test_login_required(path=reverse("vip_create", kwargs={"slug": "test_login_required"}))
    def test_tank_create_cancel(self):
        '''test the VipCreate cancel'''
        self.login()
        count = Vip.objects.count()
        data = {
            "address": "cancel",
            "city": "cancel",
            "state": "cancel",
            "cancel": True,
        }
        response = self.client.post(
            path=reverse(
                viewname="vip_create",
                kwargs={"slug": "test_login_required"}
            ),
            data=data,
            follow=True,
        )
        self.assertEqual(count, Vip.objects.count())
        self.assertEqual(0, Vip.objects.filter(address="cancel").count())
        self.assertEqual(0, Vip.objects.filter(city="cancel").count())
        self.assertEqual(0, Vip.objects.filter(state="cancel").count())
        self.assertTemplateUsed(response, "tank/vip_list.html")
        messages = list(response.context["messages"])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, WARNING)

    @test_login_required(path=reverse("vip_update", kwargs={"pk": 1}))
    def test_vip_update(self):
        '''test the VipUpdate CBV'''
        self.login()
        count = Vip.objects.count()
        response = self.client.get(
            path=reverse(
                viewname="vip_update",
                kwargs={"pk": 1}
            )
        )
        self.assertTemplateUsed(response, "tank/vip_form.html")
        self.assertContains(response, "Visual Cylinder Inspection Evaluation Form")
        self.assertEqual(count, Vip.objects.count())
        # messages = list(response.context["messages"])
        # self.assertEqual(1, len(messages))
        # self.assertEqual(messages[0].level, WARNING)

    @test_login_required(path=reverse("vip_update", kwargs={"pk": 1}))
    def test_vip_update_cancel(self):
        '''test the VipUpdate cancel'''
        self.login()
        data = {
            "address": "cancel",
            "city": "cancel",
            "state": "cancel",
            "cancel": True,
        }
        response = self.client.post(
            path=reverse(
                viewname="vip_update",
                kwargs={"pk": 1}
            ),
            data=data,
            follow=True,
        )
        self.assertEqual(0, Vip.objects.filter(address="cancel").count())
        self.assertEqual(0, Vip.objects.filter(city="cancel").count())
        self.assertEqual(0, Vip.objects.filter(state="cancel").count())
        self.assertTemplateUsed(response, "tank/vip_detail.html")
        messages = list(response.context["messages"])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, WARNING)

    @test_login_required(path=reverse("tank:eighteen_step"))
    def test_eighteen_step(self):
        '''test the eight_step FBV'''
        self.login()
        response = self.client.get(
            path=reverse(
                viewname="tank:eighteen_step",
            )
        )
        self.assertTemplateUsed(response, "tank/eighteen_step.html")
        self.assertContains(response, "PSI-PCI 18-step protocol")
