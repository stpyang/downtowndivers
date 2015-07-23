'''Copyright 2015 DDNY. All Rights Reserved.'''

from datetime import date

from django.contrib.messages.constants import INFO
from django.core.urlresolvers import reverse
from django.test import SimpleTestCase

from ddny.test_decorators import test_consent_required, test_login_required
from registration.factory import ConsentAFactory, MemberFactory
from .factory import SpecFactory, TankFactory
from .models import Hydro, Specification, Tank, Vip


class TestTankViews(SimpleTestCase):
    '''test tank views'''

    def setUp(self):
        self.member = MemberFactory.create()
        self.username = self.member.username
        self.password = "password"
        ConsentAFactory.create(member=self.member)
        if not Specification.objects.filter(slug="test_login_required").count():
            SpecFactory.create(slug="test_login_required")
        if not Tank.objects.filter(code="test_login_required").count():
            TankFactory.create(code="test_login_required")

    @test_consent_required(path=reverse("tank:create"))
    @test_login_required(path=reverse("tank:create"))
    def test_tank_create(self):
        '''test the TankCreate CBV'''
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(reverse("tank:create"))
        self.assertTemplateUsed(response, "tank/tank_form.html")
        self.assertContains(response, "Create Tank")

    @test_consent_required(path=reverse("tank:detail", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("tank:detail", kwargs={"slug": "test_login_required"}))
    def test_tank_detail(self):
        '''test the TankDetail CBV'''
        tank = TankFactory.create()
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(tank.get_absolute_url())
        self.assertTemplateUsed(response, "tank/tank_detail.html")
        self.assertContains(response, tank.code)

    @test_consent_required(path=reverse("tank:list"))
    @test_login_required(path=reverse("tank:list"))
    def test_tank_list(self):
        '''test the TankList CBV'''
        tanks = TankFactory.create_batch(10)
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(reverse("tank:list"))
        self.assertTemplateUsed(response, "tank/tank_list.html")
        for t in tanks:
            self.assertContains(response, t.code)
            self.assertContains(response, t.doubles_code)
            self.assertContains(response, t.spec.name)
            self.assertContains(response, t.owner)
            if t.last_hydro:
                self.assertContains(response, t.last_hydro.strftime("%Y-%m-%d"))
            if t.last_vip:
                self.assertContains(response, t.last_vip.strftime("%Y-%m-%d"))

    @test_consent_required(path=reverse("tank:update", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("tank:update", kwargs={"slug": "test_login_required"}))
    def test_tank_update(self):
        '''test the TankUpdate CBV'''
        count = Tank.objects.count()
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(
            path=reverse(
                "tank:update",
                kwargs={"slug": "test_login_required"}
            )
        )
        self.assertTemplateUsed(response, "tank/tank_form.html")
        self.assertContains(response, "Update test_login_required")
        self.assertEquals(count, Tank.objects.count())

    @test_consent_required(path=reverse("tank:create"))
    @test_login_required(path=reverse("tank:create"))
    def test_tank_create_form(self):
        '''test the TankCreate Form'''
        count = Tank.objects.count()
        spec = SpecFactory.create()
        tank = TankFactory.build()
        form = {
            "serial_number": tank.serial_number,
            "code": tank.code,
            "owner": self.member.id,
            "spec": spec.id,
            "hydro_set-0-date": "",
            "vip_set-0-date": "",
            "hydro_set-TOTAL_FORMS": 1,
            "hydro_set-INITIAL_FORMS": 0,
            "hydro_set-MIN_NUM_FORMS": 0,
            "hydro_set-MAX_NUM_FORMS": 1000,
            "vip_set-TOTAL_FORMS": 1,
            "vip_set-INITIAL_FORMS": 0,
            "vip_set-MIN_NUM_FORMS": 0,
            "vip_set-MAX_NUM_FORMS": 1000,
        }
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.post(
            path=reverse("tank:create"),
            data=form,
            follow=True,
        )
        self.assertEquals(count + 1, Tank.objects.count())
        messages = list(response.context["messages"])
        self.assertEquals(1, len(messages))
        self.assertEqual(messages[0].level, INFO)

    @test_consent_required(path=reverse("tank:create"))
    @test_login_required(path=reverse("tank:create"))
    def test_tank_create_form_hydro_vip(self):
        '''test the TankCreate Form with HydroInline and VipInline'''
        tank_count = Tank.objects.count()
        hydro_count = Hydro.objects.count()
        vip_count = Vip.objects.count()
        spec = SpecFactory.create()
        tank = TankFactory.build()
        form = {
            "serial_number": tank.serial_number,
            "code": tank.code,
            "owner": self.member.id,
            "spec": spec.id,
            "hydro_set-0-date": date.today().strftime("%Y-%m-%d"),
            "vip_set-0-date": date.today().strftime("%Y-%m-%d"),
            "hydro_set-TOTAL_FORMS": 1,
            "hydro_set-INITIAL_FORMS": 0,
            "hydro_set-MIN_NUM_FORMS": 0,
            "hydro_set-MAX_NUM_FORMS": 1000,
            "vip_set-TOTAL_FORMS": 1,
            "vip_set-INITIAL_FORMS": 0,
            "vip_set-MIN_NUM_FORMS": 0,
            "vip_set-MAX_NUM_FORMS": 1000,
        }
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.post(
            path=reverse("tank:create"),
            data=form,
            follow=True)
        self.assertEquals(tank_count + 1, Tank.objects.count())
        self.assertEquals(hydro_count + 1, Hydro.objects.count())
        self.assertEquals(vip_count + 1, Vip.objects.count())
        messages = list(response.context["messages"])
        self.assertEquals(1, len(messages))
        self.assertEqual(messages[0].level, INFO)

    # TODO(stpyang): fix
    # @test_login_required(path=reverse("tank:update"))
    # @test_consent_required(path=reverse("tank:update"))
    def test_tank_update_form(self):
        '''test the TankUpdate Form'''
        tank = TankFactory.create()
        count = Tank.objects.count()
        form = {
            "serial_number": tank.serial_number,
            "code": tank.code,
            "owner": self.member.id,
            "spec": tank.spec.id,
            "hydro_set-0-date": "",
            "vip_set-0-date": "",
            "hydro_set-TOTAL_FORMS": 1,
            "hydro_set-INITIAL_FORMS": 0,
            "hydro_set-MIN_NUM_FORMS": 0,
            "hydro_set-MAX_NUM_FORMS": 1000,
            "vip_set-TOTAL_FORMS": 1,
            "vip_set-INITIAL_FORMS": 0,
            "vip_set-MIN_NUM_FORMS": 0,
            "vip_set-MAX_NUM_FORMS": 1000,
        }
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.post(
            path=reverse("tank:update", kwargs={"slug": tank.code}),
            data=form,
            follow=True
        )
        self.assertEquals(count, Tank.objects.count())
        messages = list(response.context["messages"])
        self.assertEquals(1, len(messages))
        self.assertEqual(messages[0].level, INFO)


class TestSpecViews(SimpleTestCase):
    '''test spec views'''

    def setUp(self):
        self.member = MemberFactory.create()
        self.username = self.member.username
        self.password = "password"
        ConsentAFactory.create(member=self.member)
        if not Specification.objects.filter(name="test_login_required").count():
            SpecFactory.create(name="test_login_required")

    @test_consent_required(path=reverse("tank:spec_create"))
    @test_login_required(path=reverse("tank:spec_create"))
    def test_spec_create(self):
        '''test the SpecCreate CBV'''
        count = Specification.objects.count()
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(reverse("tank:spec_create"))
        self.assertTemplateUsed(response, "tank/spec_form.html")
        self.assertContains(response, "Create Spec")
        self.assertEquals(count, Specification.objects.count())

    @test_consent_required(path=reverse("tank:spec_detail", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("tank:spec_detail", kwargs={"slug": "test_login_required"}))
    def test_spec_detail(self):
        '''test the SpecDetail CBV'''
        spec = SpecFactory.create()
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(spec.get_absolute_url())
        self.assertTemplateUsed(response, "tank/spec_detail.html")
        self.assertContains(response, spec.name)

    @test_consent_required(path=reverse("tank:spec_list"))
    @test_login_required(path=reverse("tank:spec_list"))
    def test_spec_list(self):
        '''test the SpecList CBV'''
        specs = SpecFactory.create_batch(10)
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(reverse("tank:spec_list"))
        self.assertTemplateUsed(response, "tank/spec_list.html")
        for s in specs:
            self.assertContains(response, s.name)
            self.assertContains(response, s.metal)
            self.assertContains(response, "{0:.1f}".format(s.volume))
            self.assertContains(response, s.pressure)
            self.assertContains(response, "{0:.1f}".format(s.tank_factor))

    @test_consent_required(path=reverse("tank:spec_update", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("tank:spec_update", kwargs={"slug": "test_login_required"}))
    def test_spec_update(self):
        '''test the SpecUpdate CBV'''
        count = Specification.objects.count()
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(
            path=reverse(
                "tank:spec_update",
                kwargs={"slug": "test_login_required"}
            )
        )
        self.assertTemplateUsed(response, "tank/spec_form.html")
        self.assertContains(response, "Update test_login_required")
        self.assertEquals(count, Specification.objects.count())

    @test_consent_required(path=reverse("tank:spec_create"))
    @test_login_required(path=reverse("tank:spec_create"))
    def test_spec_create_form(self):
        '''test the SpecCreate Form'''
        count = Specification.objects.count()
        spec = SpecFactory.build()
        form = {
            "name": spec.name,
            "metal": spec.metal,
            "volume": spec.volume,
            "pressure": spec.pressure,
        }
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.post(
            path=reverse("tank:spec_create"),
            data=form,
            follow=True
        )
        self.assertEquals(count + 1, Specification.objects.count())
        messages = list(response.context["messages"])
        self.assertEquals(1, len(messages))
        self.assertEqual(messages[0].level, INFO)

    # TODO(stpyang): fix
    # @test_login_required(path=reverse("tank:spec_update"))
    # @test_consent_required(path=reverse("tank:spec_update"))
    def test_spec_update_form(self):
        '''test the SpecUpdate Form'''
        spec = SpecFactory.create()
        count = Specification.objects.count()
        form = {
            "name": spec.name,
            "metal": spec.metal,
            "volume": spec.volume,
            "pressure": spec.pressure,
        }
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.post(
            path=reverse("tank:spec_update", kwargs={"slug": spec.slug}),
            data=form,
            follow=True
        )
        self.assertEquals(count, Specification.objects.count())
        messages = list(response.context["messages"])
        self.assertEquals(1, len(messages))
        self.assertEqual(messages[0].level, INFO)
