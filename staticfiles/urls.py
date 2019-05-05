'''ddny URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  path('blog/', include(blog_urls))
'''

from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, re_path, include

from ddny import views as ddny_views
from tank import views as tank_views

from registration import views as registration_views

urlpatterns = [
    #google chrome favicon fix
    path('favicon.ico/',
         lambda x: HttpResponseRedirect(settings.STATIC_URL + 'static/ddny/images/favicon.ico')),
    # ADMIN PAGES #
    path('admin/',
         admin.site.urls),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    # REGISTRATION PAGES #
    path('login/',
         registration_views.login,
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         {'template_name': 'registration/password_reset_done.html'},
         name='password_reset_done'),
    # TANK PAGES #
    path('spec/create/',
         view=tank_views.SpecCreate.as_view(),
         name='spec_create'),
    path('spec/<slug:slug>/',
         view=tank_views.SpecDetail.as_view(),
         name='spec_detail'),
    path('spec/update/<slug:slug>/',
         view=tank_views.SpecUpdate.as_view(),
         name='spec_update'),
    path('spec/',
         view=tank_views.SpecList.as_view(),
         name='spec_list'),
    path('vip/create/<slug:slug>/',
         view=tank_views.VipCreate.as_view(),
         name='vip_create'),
    re_path(r'vip/update/(?P<pk>\d+)/',
            view=tank_views.VipUpdate.as_view(),
            name='vip_update'),
    re_path(r'vip/(?P<pk>\d+)/',
            view=tank_views.VipDetail.as_view(),
            name='vip_detail'),
    path('vip/',
         view=tank_views.VipList.as_view(),
         name='vip_list'),
    # TODO(stpyang): fix
    re_path(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
            auth_views.PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    # TODO(stpyang): fix
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    # MY APPS #
    path('grappelli/', include('grappelli.urls')),
    path('ddny_braintree/', include(('ddny_braintree.urls', 'braintree'), namespace='braintree')),
    path('ddny_calendar/', include(('ddny_calendar.urls', 'ddny_calendar'),
         namespace='ddny_calendar')),
    path('debug/', include(('debug.urls', 'debug'), namespace='debug')),
    path('fillstation/', include(('fillstation.urls', 'fillstation'), namespace='fillstation')),
    path('gas/', include(('gas.urls', 'gas'), namespace='gas')),
    path('tank/', include(('tank.urls', 'tanks'), namespace='tank')),
    # HOME
    path('contact_info/', ddny_views.contact_info, name='contact_info'),
    path('club_dues/', ddny_views.club_dues, name='club_dues'),
    path('', ddny_views.home, name='home'),
    path('privacy_policy/', ddny_views.privacy_policy, name='privacy_policy'),
    path('refund_policy/', ddny_views.refund_policy, name='refund_policy'),
    # registration stuff
    path('consent_form/',
         view=registration_views.ConsentACreate.as_view(),
         name='consent_form'),
    re_path(r'consent/(?P<pk>\d+)/',
            view=registration_views.ConsentADetail.as_view(),
            name='consent_detail'),
    path('dues/<slug:slug>/',
         view=registration_views.pay_dues,
         name='pay_dues'),
    path('members/',
         view=registration_views.MemberList.as_view(),
         name='member_list'),
    path('update_profile/<slug:slug>/',
         view=registration_views.MemberUpdate.as_view(),
         name='member_update'),
    path('<slug:slug>/',
         view=registration_views.MemberDetail.as_view(),
         name='member_detail'),
]
