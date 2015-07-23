'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.conf.urls import url

from . import views


urlpatterns = [
    url(regex=r"^spec/create/$",
        view=views.SpecCreate.as_view(),
        name="spec_create"),
    url(regex=r"^spec/(?P<slug>[\w-]+)/$",
        view=views.SpecDetail.as_view(),
        name="spec_detail"),
    url(regex=r"^spec/$",
        view=views.SpecList.as_view(),
        name="spec_list"),
    url(regex=r"spec/update/(?P<slug>[\w-]+)/$",
        view=views.SpecUpdate.as_view(),
        name="spec_update"),
    url(regex=r"^create/$",
        view=views.TankCreate.as_view(),
        name="create"),
    url(regex=r"^(?P<slug>[\w-]+)/$",
        view=views.TankDetail.as_view(),
        name="detail"),
    url(regex=r"^$",
        view=views.TankList.as_view(),
        name="list"),
    url(regex=r"update/(?P<slug>[\w-]+)/$",
        view=views.TankUpdate.as_view(),
        name="update"),
]
