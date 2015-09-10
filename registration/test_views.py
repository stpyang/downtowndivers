'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.contrib.messages.constants import INFO
from django.core.urlresolvers import reverse
from django.test import SimpleTestCase
from django.utils.html import escape

from ddny.test_decorators import test_consent_required, test_login_required
from .factory import ConsentAFactory, MemberFactory, RandomUserFactory
from .models import Member

class TestMemberViews(SimpleTestCase):
    '''test views'''

    def setUp(self):
        self.member = MemberFactory.create()
        self.username = self.member.username
        self.password = "password"
        self.user = self.member.user
        self.consent = ConsentAFactory.create(member=self.member)

    @test_consent_required(path=reverse("consent_form"))
    @test_login_required(path=reverse("consent_form"))
    def test_consent_detail(self):
        '''test the ConsentDetail CBV'''
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(
            path=reverse(
                "consent_detail",
                kwargs={"pk": self.consent.id}
            )
        )
        self.assertTemplateUsed(response, "registration/consenta_detail.html")

    @test_login_required(path=reverse("consent_form"))
    def test_consent_form(self):
        '''test the ConsentCreate CBV'''
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(reverse("consent_form"))
        self.assertTemplateUsed(response, "registration/consenta_form.html")
        self.assertContains(response, "DDNY liability release and assumption of risk agreement")
        self.assertContains(response, escape(self.member.full_name), 2)

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
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(self.member.get_absolute_url())
        self.assertTemplateUsed(response, "registration/member_detail.html")
        self.assertContains(response, escape(self.member.full_name))

    @test_consent_required(path=reverse("member_list"))
    @test_login_required(path=reverse("member_list"))
    def test_member_list(self):
        '''test the MemberList CBV'''
        members = MemberFactory.create_batch(10)
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(reverse("member_list"))
        self.assertTemplateUsed(response, "registration/member_list.html")
        for m in members:
            self.assertContains(response, escape(m.first_name))
            self.assertContains(response, escape(m.last_name))

    @test_consent_required(path=reverse("member_update", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("member_update", kwargs={"slug": "test_login_required"}))
    def test_member_update(self):
        '''test the MemberUpdate CBV'''
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(
            path=reverse(
                "member_update",
                kwargs={"slug": self.member.slug}
            )
        )
        self.assertTemplateUsed(response, "registration/member_form.html")
        self.assertContains(response, "Update {0}".format(self.username))

    @test_consent_required(path=reverse("member_update", kwargs={"slug": "test_login_required"}))
    @test_login_required(path=reverse("member_update", kwargs={"slug": "test_login_required"}))
    def test_member_update_permissiondenied(self):
        '''test the MemberUpdate CBV permissions'''
        user = RandomUserFactory.create(username="test_member_update_permissiond")
        member = MemberFactory.create(user=user)
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(
            path=reverse(
                "member_update",
                kwargs={"slug": member.slug}
            )
        )
        self.assertEquals(403, response.status_code)

    def test_member_update_form(self):
        '''test the MemberUpdate Form'''
        count = Member.objects.count()
        form = {
            "username": self.username,
            "first_name": self.member.first_name,
            "last_name": self.member.last_name,
            "email": self.member.email,
        }
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.post(
            path=reverse("member_update", kwargs={"slug": self.member.slug}),
            data=form,
            follow=True,
        )
        self.assertEquals(count, Member.objects.count())
        messages = list(response.context["messages"])
        self.assertEquals(1, len(messages))
        self.assertEqual(messages[0].level, INFO)

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
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get("/password_change/")
        self.assertTemplateUsed(response, "registration/password_change.html")

    @test_consent_required(path=reverse("password_change_success"))
    @test_login_required(path=reverse("password_change_success"))
    def test_password_change_success(self):
        '''test that the password_change_success page loads'''
        self.assertEquals(
            True,
            self.client.login(username=self.username, password=self.password)
        )
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
