'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.contrib.messages.constants import SUCCESS, WARNING
from django.urls import reverse
from django.utils.html import escape

from ddny.test_decorators import test_consent_required, test_login_required
from ddny.test_views import BaseDdnyTestCase
from .factory import MemberFactory, RandomUserFactory
from .models import Member


class TestMemberViews(BaseDdnyTestCase):
    '''https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TestCase'''

    @test_consent_required(path=reverse('member_update', kwargs={'slug': 'test_login_required'}))
    @test_login_required(path=reverse('member_update', kwargs={'slug': 'test_login_required'}))
    def test_consent_form_superuser(self):
        '''test the ConsentCreate CBV'''
        user = RandomUserFactory.create(is_superuser=True)
        self.assertEqual(
            True,
            self.client.login(username=user.username, password=self.password)
        )
        response = self.client.get(reverse('consent_form'))
        self.assertEqual(404, response.status_code)

    @test_consent_required(path=reverse('member_update', kwargs={'slug': 'test_login_required'}))
    @test_login_required(path=reverse('member_update', kwargs={'slug': 'test_login_required'}))
    def test_member_detail(self):
        '''test the MemberDetail CBV'''
        self.login()
        response = self.client.get(self.member.get_absolute_url())
        self.assertTemplateUsed(response, 'registration/member_detail.html')
        self.assertContains(response, escape(self.member.full_name))
        self.assertContains(response,
                            'Member since {0}'.format(self.member.member_since))

    @test_consent_required(path=reverse('member_update', kwargs={'slug': 'test_login_required'}))
    @test_login_required(path=reverse('member_update', kwargs={'slug': 'test_login_required'}))
    def test_member_list(self):
        '''test the MemberList CBV'''
        members = MemberFactory.create_batch(10)
        self.login()
        response = self.client.get(reverse('member_list'))
        self.assertTemplateUsed(response, 'registration/member_list.html')
        for member in members:
            self.assertContains(response, escape(member.first_name))
            self.assertContains(response, escape(member.last_name))
            self.assertContains(response, member.email)
            self.assertContains(response, member.phone_number)

    @test_consent_required(path=reverse('member_update', kwargs={'slug': 'test_login_required'}))
    @test_login_required(path=reverse('member_update', kwargs={'slug': 'test_login_required'}))
    def test_member_update(self):
        '''test the MemberUpdate CBV'''
        self.login()
        response = self.client.get(
            path=reverse(
                viewname='member_update',
                kwargs={'slug': self.member.slug}
            )
        )
        self.assertTemplateUsed(response, 'registration/member_form.html')
        self.assertContains(response, 'Update profile: {0}'.format(self.username))

    @test_consent_required(path=reverse('member_list'))
    @test_login_required(path=reverse('member_list'))
    def test_member_update_permissiondenied(self):
        '''test the MemberUpdate CBV permissions'''
        user = RandomUserFactory.create(username='test_member_update_permissiond')
        member = MemberFactory.create(user=user)
        self.login()
        response = self.client.get(
            path=reverse(
                viewname='member_update',
                kwargs={'slug': member.slug}
            )
        )
        self.assertEqual(404, response.status_code)

    @test_consent_required(path=reverse('member_detail', kwargs={'slug': 'test_login_required'}))
    @test_login_required(path=reverse('member_detail', kwargs={'slug': 'test_login_required'}))
    def test_member_update_form(self):
        '''test the MemberUpdate Form'''
        count = Member.objects.count()
        form = {
            'username': self.username,
            'first_name': self.member.first_name,
            'last_name': self.member.last_name,
            'email': self.member.email,
            'gender': self.member.gender,
        }
        self.login()
        response = self.client.post(
            path=reverse('member_update', kwargs={'slug': self.member.slug}),
            data=form,
            follow=True,
        )
        self.assertEqual(count, Member.objects.count())
        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, SUCCESS)

    @test_consent_required(path=reverse('consent_form'))
    @test_login_required(path=reverse('consent_form'))
    def test_member_update_cancel(self):
        '''test the MemberUpdate cancel'''
        data = {
            'username': 'cancel',
            'first_name': 'cancel',
            'last_name': 'cancel',
            'cancel': True,
        }
        self.login()
        response = self.client.post(
            path=reverse('member_update', kwargs={'slug': self.member.slug}),
            data=data,
            follow=True,
        )
        self.assertEqual(0, Member.objects.filter(username='cancel').count())
        self.assertEqual(0, Member.objects.filter(first_name='cancel').count())
        self.assertEqual(0, Member.objects.filter(last_name='cancel').count())
        self.assertTemplateUsed(response, 'registration/member_detail.html')
        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].level, WARNING)

    def test_login(self):
        ''' test that the login page loads '''
        response = self.client.get('')
        self.assertRedirects(
            response,
            expected_url='/login/?next=/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logout(self):
        ''' test that the logout page loads '''
        response = self.client.get('/logout/')
        self.assertTemplateUsed(response, 'registration/logged_out.html')

    @test_consent_required(path=reverse('password_change'))
    @test_login_required(path=reverse('password_change'))
    def test_password_change(self):
        '''test that the password_change page loads'''
        self.login()
        response = self.client.get('/password_change/')
        self.assertTemplateUsed(response, 'registration/password_change_form.html')

    @test_consent_required(path=reverse('password_change'))
    @test_login_required(path=reverse('password_change'))
    def test_password_change_done(self):
        '''test that the password_change_done page loads'''
        self.login()
        response = self.client.get('/password_change/done/')
        self.assertTemplateUsed(response, 'registration/password_change_done.html')

    def test_password_reset(self):
        ''' test that the password_reset page loads '''
        response = self.client.get('/password_reset/')
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')

    def test_password_reset_done(self):
        ''' test that the password_reset_done page loads '''
        response = self.client.get('/password_reset/done/')
        self.assertTemplateUsed(response, 'registration/password_reset_done.html')
