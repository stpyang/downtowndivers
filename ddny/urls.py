'''ddny URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r"^$", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r"^$", Home.as_view(), name="home")
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r"^blog/", include(blog_urls))
'''

from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.http import HttpResponseRedirect

from ddny import views as ddny_views

from registration import views as registration_views

urlpatterns = [
    #google chrome favicon fix
    url(r'^favicon.ico/$',
        lambda x: HttpResponseRedirect(settings.STATIC_URL + "static/ddny/images/favicon.ico")),
    # ADMIN PAGES #
    url(r"^admin/",
        include(admin.site.urls)),
    url(r"^password_change/done/$",
        auth_views.password_change_done,
        name="password_change_done"),
    url(r"^password_reset/done/$",
        auth_views.password_reset_done,
        name="password_reset_done"),
    # REGISTRATION PAGES #
    url(r"^signin/$",
        registration_views.login,
        {"template_name": "registration/signin.html"},
        name="signin"),
    url(r"^signout/$",
        auth_views.logout,
        {"template_name": "registration/signout.html"},
        name="signout"),
    url(r"^password_change/$",
        registration_views.password_change,
        {"template_name": "registration/password_change.html",
         "post_change_redirect": "/password_change/success"},
        name="password_change"),
    url(r"^password_change/success/$",
        registration_views.password_change_done,
        {"template_name": "registration/password_change_success.html"},
        name="password_change_success"),
    url(r"^password_reset/$",
        auth_views.password_reset,
        {"template_name": "registration/password_reset.html",
         "post_reset_redirect": "/password_reset/success"},
        name="password_reset"),
    url(r"^password_reset/success/$",
        auth_views.password_reset_done,
        {"template_name": "registration/password_reset_success.html"},
        name="password_reset_success"),
    # TODO(stpyang): fix
    url(r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.password_reset_confirm,
        name="password_reset_confirm"),
    # TODO(stpyang): fix
    url(r"^reset/done/$", auth_views.password_reset_complete,
        name="password_reset_complete"),
    # MY APPS #
    url(r"^grappelli/", include("grappelli.urls")),
    url(r"^ddny_braintree/", include("ddny_braintree.urls", namespace="braintree")),
    url(r"^debug/", include("debug.urls", namespace="debug")),
    url(r"^fillstation/", include("fillstation.urls", namespace="fillstation")),
    url(r"^gas/", include("gas.urls", namespace="gas")),
    url(r"^tank/", include("tank.urls", namespace="tank")),
    # HOME
    url(r"^contact_info/$", ddny_views.contact_info, name="contact_info"),
    url(r"^club_dues/$", ddny_views.club_dues, name="club_dues"),
    url(r"^$", ddny_views.home, name="home"),
    url(r"^privacy_policy/$", ddny_views.privacy_policy, name="privacy_policy"),
    url(r"^refund_policy/$", ddny_views.refund_policy, name="refund_policy"),
    # registration stuff
    url(regex=r"^consent_form/$",
        view=registration_views.ConsentACreate.as_view(),
        name="consent_form"),
    url(regex=r"^consent/(?P<pk>\d+)/$",
        view=registration_views.ConsentADetail.as_view(),
        name="consent_detail"),
    url(regex=r"^members/$",
        view=registration_views.MemberList.as_view(),
        name="member_list"),
    url(regex=r"^update_profile/(?P<slug>[\w-]+)/$",
        view=registration_views.MemberUpdate.as_view(),
        name="member_update"),
    url(regex=r"^(?P<slug>[\w-]+)/$",
        view=registration_views.MemberDetail.as_view(),
        name="member_detail"),
]
