'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.conf.urls import url

from . import views


urlpatterns = [
    url(regex=r"^create/$",
        view=views.TankCreate.as_view(),
        name="create"),
    url(regex=r"^eighteen_step/$",
        view=views.eighteen_step,
        name="eighteen_step"),
    url(regex=r"^$",
        view=views.TankList.as_view(),
        name="list"),
    url(regex=r"update/(?P<slug>[\w-]+)/$",
        view=views.TankUpdate.as_view(),
        name="update"),
    url(regex=r"^(?P<slug>[\w-]+)/$",
        view=views.TankDetail.as_view(),
        name="detail"),
]
