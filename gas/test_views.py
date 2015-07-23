'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.core.urlresolvers import reverse
from django.test import SimpleTestCase

from ddny.test_decorators import test_consent_required, test_login_required
from registration.factory import ConsentAFactory, MemberFactory
from .factory import GasFactory

class TestGasViews(SimpleTestCase):
    '''test views'''

    def setUp(self):
        self.member = MemberFactory.create()
        self.username = self.member.username
        self.password = "password"
        ConsentAFactory.create(member=self.member)
        GasFactory.create(slug="test_login_required")

    @test_consent_required(path=reverse("gas:detail", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("gas:detail", kwargs={"slug": "test_login_required"}))
    def test_gas_detail(self):
        '''test the GasDetail CBV'''
        gas = GasFactory.create()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse(
                "gas:detail",
                kwargs={"slug": gas.slug,},
            )
        )

        self.assertTemplateUsed(response, "gas/gas_detail.html")
        self.assertContains(response, gas.name)

    @test_consent_required(path=reverse("gas:list"))
    @test_login_required(path=reverse("gas:list"))
    def test_gas_list(self):
        '''test the GasList CBV'''
        gases = GasFactory.create_batch(10)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("gas:list"))
        self.assertTemplateUsed(response, "gas/gas_list.html")
        for g in gases:
            self.assertContains(response, g.name)
            self.assertContains(response, "{0:.2f}".format(g.cost))
