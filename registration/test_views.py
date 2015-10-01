'''Copyright 2015 DDNY. All Rights Reserved.'''

from datetime import date
import json

from django.contrib.messages.constants import INFO, WARNING
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory
from django.utils.html import escape

from ddny.test_decorators import test_consent_required, test_login_required
from ddny.test_views import BaseDdnyTestCase
from .factory import MemberFactory, RandomUserFactory
from .models import Member, ConsentA

class TestMemberViews(BaseDdnyTestCase):
    '''test views'''

    @test_consent_required(path=reverse("pay_dues", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("pay_dues", kwargs={"slug": "test_login_required"}))
    def test_pay_dues(self):
        '''test the pay_dues view'''
        self.login()
        response = self.client.get(
            path=reverse(
                viewname="pay_dues",
                kwargs={"slug": self.member.slug}
            )
        )
        self.assertTemplateUsed(response, "registration/pay_dues.html")

    @test_consent_required(path=reverse("pay_dues", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("pay_dues", kwargs={"slug": "test_login_required"}))
    def test_pay_dues_permissions(self):
        '''test the members cannot load the pay_dues page for other members'''
        self.login()
        user = RandomUserFactory.create(username="test_pay_dues_permission")
        random_member = MemberFactory.create(user=user)
        response = self.client.get(
            path=reverse(
                viewname="pay_dues",
                kwargs={"slug": random_member.slug}
            )
        )
        self.assertEquals(403, response.status_code)

    @test_consent_required(path=reverse("consent_form"))
    @test_login_required(path=reverse("consent_form"))
    def test_consent_detail(self):
        '''test the ConsentDetail CBV'''
        self.login()
        response = self.client.get(
            path=reverse(
                viewname="consent_detail",
                kwargs={"pk": self.consent.id}
            )
        )
        self.assertTemplateUsed(response, "registration/consenta_detail.html")

    @test_login_required(path=reverse("consent_form"))
    def test_consent_form(self):
        '''test the ConsentCreate CBV'''
        self.login()
        response = self.client.get(reverse("consent_form"))
        self.assertTemplateUsed(response, "registration/consenta_form.html")
        self.assertContains(response, "DDNY liability release and assumption of risk agreement")
        self.assertContains(response, escape(self.member.full_name), 2)

    @test_login_required(path=reverse("consent_form"))
    def test_consent_create(self):
        '''test the ConsentCreate CBV'''
        self.login()
        count = ConsentA.objects.count()
        data = {
            "member": self.member.id,
            "member_name": self.member.full_name,
            "member_signature": json.dumps([{"x": [1, 2], "y": [3, 4]}]),
            "member_signature_date": date.today().strftime("%Y-%m-%d"),
            "witness_name": self.member.full_name,
            "witness_signature": json.dumps([{"x": [1, 2], "y": [3, 4]}]),
            "witness_signature_date": date.today().strftime("%Y-%m-%d"),
            "consent_is_experienced_certified_diver": True,
            "consent_club_is_non_profit": True,
            "consent_vip_tank": True,
            "consent_examine_tank": True,
            "consent_no_unsafe_tank": True,
            "consent_analyze_gas": True,
            "consent_compressed_gas_risk": True,
            "consent_diving_risk": True,
            "consent_sole_responsibility": True,
            "consent_do_not_sue": True,
            "consent_strenuous_activity_risk": True,
            "consent_inspect_equipment": True,
            "consent_lawful_age": True,
            "consent_release_of_risk": True,
        }
        Form = modelform_factory(ConsentA, fields=data)
        self.assertTrue(Form(data).is_valid())
        response = self.client.post(
            path=reverse("consent_form"),
            data=data,
            follow=True,
        )
        self.assertEquals(count + 1, ConsentA.objects.count())
        messages = list(response.context["messages"])
        self.assertEquals(1, len(messages))
        self.assertEqual(messages[0].level, INFO)

    @test_login_required(path=reverse("consent_form"))
    def test_consent_form_superuser(self):
        '''test the ConsentCreate CBV'''
        user = RandomUserFactory.create(is_superuser=True)
        self.assertEquals(
            True,
            self.client.login(username=user.username, password=self.password)
        )
        response = self.client.get(reverse("consent_form"))
        self.assertEquals(404, response.status_code)

    @test_consent_required(path=reverse("member_detail", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("member_detail", kwargs={"slug": "test_login_required"}))
    def test_member_detail(self):
        '''test the MemberDetail CBV'''
        self.login()
        response = self.client.get(self.member.get_absolute_url())
        self.assertTemplateUsed(response, "registration/member_detail.html")
        self.assertContains(response, escape(self.member.full_name))
        self.assertContains(response,
                            "Member since {0}".format(self.member.member_since))

    @test_consent_required(path=reverse("member_list"))
    @test_login_required(path=reverse("member_list"))
    def test_member_list(self):
        '''test the MemberList CBV'''
        members = MemberFactory.create_batch(10)
        self.login()
        response = self.client.get(reverse("member_list"))
        self.assertTemplateUsed(response, "registration/member_list.html")
        for m in members:
            self.assertContains(response, escape(m.first_name))
            self.assertContains(response, escape(m.last_name))
            self.assertContains(response, m.email)
            self.assertContains(response, m.phone_number)

    @test_consent_required(path=reverse("member_update", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("member_update", kwargs={"slug": "test_login_required"}))
    def test_member_update(self):
        '''test the MemberUpdate CBV'''
        self.login()
        response = self.client.get(
            path=reverse(
                viewname="member_update",
                kwargs={"slug": self.member.slug}
            )
        )
        self.assertTemplateUsed(response, "registration/member_form.html")
        self.assertContains(response, "Update profile: {0}".format(self.username))

    @test_consent_required(path=reverse("member_update", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("member_update", kwargs={"slug": "test_login_required"}))
    def test_member_update_permissiondenied(self):
        '''test the MemberUpdate CBV permissions'''
        user = RandomUserFactory.create(username="test_member_update_permissiond")
        member = MemberFactory.create(user=user)
        self.login()
        response = self.client.get(
            path=reverse(
                viewname="member_update",
                kwargs={"slug": member.slug}
            )
        )
        self.assertEquals(404, response.status_code)

    @test_consent_required(path=reverse("member_update", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("member_update", kwargs={"slug": "test_login_required"}))
    def test_member_update_form(self):
        '''test the MemberUpdate Form'''
        count = Member.objects.count()
        form = {
            "username": self.username,
            "first_name": self.member.first_name,
            "last_name": self.member.last_name,
            "email": self.member.email,
            "gender": self.member.gender,
        }
        self.login()
        response = self.client.post(
            path=reverse("member_update", kwargs={"slug": self.member.slug}),
            data=form,
            follow=True,
        )
        self.assertEquals(count, Member.objects.count())
        messages = list(response.context["messages"])
        self.assertEquals(1, len(messages))
        self.assertEqual(messages[0].level, INFO)

    @test_consent_required(path=reverse("member_update", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("member_update", kwargs={"slug": "test_login_required"}))
    def test_member_update_cancel(self):
        '''test the MemberUpdate cancel'''
        data = {
            "username": "cancel",
            "first_name": "cancel",
            "last_name": "cancel",
            "cancel": True,
        }
        self.login()
        response = self.client.post(
            path=reverse("member_update", kwargs={"slug": self.member.slug}),
            data=data,
            follow=True,
        )
        self.assertEquals(0, Member.objects.filter(username="cancel").count())
        self.assertEquals(0, Member.objects.filter(first_name="cancel").count())
        self.assertEquals(0, Member.objects.filter(last_name="cancel").count())
        self.assertTemplateUsed(response, "registration/member_detail.html")
        messages = list(response.context["messages"])
        self.assertEquals(1, len(messages))
        self.assertEqual(messages[0].level, WARNING)

    def test_signin(self):
        ''' test that the signin page loads '''
        response = self.client.get("")
        self.assertRedirects(
            response,
            expected_url="signin/?next=/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        response = self.client.get("/signin/")
        self.assertTemplateUsed(response, "registration/signin.html")

    def test_signout(self):
        ''' test that the signout page loads '''
        response = self.client.get("/signout/")
        self.assertTemplateUsed(response, "registration/signout.html")

    @test_consent_required(path=reverse("password_change"))
    @test_login_required(path=reverse("password_change"))
    def test_password_change(self):
        '''test that the password_change page loads'''
        self.login()
        response = self.client.get("/password_change/")
        self.assertTemplateUsed(response, "registration/password_change.html")

    @test_consent_required(path=reverse("password_change_success"))
    @test_login_required(path=reverse("password_change_success"))
    def test_password_change_success(self):
        '''test that the password_change_success page loads'''
        self.login()
        response = self.client.get("/password_change/success/")
        self.assertTemplateUsed(response, "registration/password_change_success.html")

    def test_password_reset(self):
        ''' test that the password_reset page loads '''
        response = self.client.get("/password_reset/")
        self.assertTemplateUsed(response, "registration/password_reset.html")

    def test_password_reset_done(self):
        ''' test that the password_reset_success page loads '''
        response = self.client.get("/password_reset/success/")
        self.assertTemplateUsed(response, "registration/password_reset_success.html")
