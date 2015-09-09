'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.core.urlresolvers import reverse

from ddny.test_decorators import test_consent_required, test_login_required
from ddny.test_views import BaseDdnyTestCase
from .factory import GasFactory
from .models import Gas


class TestGasViews(BaseDdnyTestCase):
    '''test views'''

    def setUp(self):
        super(TestGasViews, self).setUp()
        if not Gas.objects.filter(slug="test_login_required").count():
            GasFactory.create(slug="test_login_required")

    @test_consent_required(path=reverse("gas:detail", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("gas:detail", kwargs={"slug": "test_login_required"}))
    def test_gas_detail(self):
        '''test the GasDetail CBV'''
        self.login()
        gas = GasFactory.create()
        response = self.client.get(
            reverse(
                viewname="gas:detail",
                kwargs={"slug": gas.slug,},
            )
        )

        self.assertTemplateUsed(response, "gas/gas_detail.html")
        self.assertContains(response, gas.name)

    @test_consent_required(path=reverse("gas:list"))
    @test_login_required(path=reverse("gas:list"))
    def test_gas_list(self):
        '''test the GasList CBV'''
        self.login()
        gases = GasFactory.create_batch(10)
        response = self.client.get(reverse("gas:list"))
        self.assertTemplateUsed(response, "gas/gas_list.html")
        for g in gases:
            self.assertContains(response, g.name)
            self.assertContains(response, "{0:.2f}".format(g.cost))
