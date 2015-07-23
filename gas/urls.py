'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.conf.urls import url

from . import views


urlpatterns = [
    url(regex=r"^(?P<slug>[\w-]+)/$",
        view=views.GasDetail.as_view(),
        name="detail"),
    url(regex=r"^$",
        view=views.GasList.as_view(),
        name="list"),
]
