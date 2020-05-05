'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.urls import path

from . import views


urlpatterns = [  # pylint: disable=invalid-name
    path("create/",
         view=views.TankCreate.as_view(),
         name="create"),
    path('download/',
         view=views.download,
         name='download'),
    path("eighteen_step/",
         view=views.eighteen_step,
         name="eighteen_step"),
    path("",
         view=views.TankList.as_view(),
         name="list"),
    path("update/<slug:slug>/",
         view=views.TankUpdate.as_view(),
         name="update"),
    path("<slug:slug>/",
         view=views.TankDetail.as_view(),
         name="detail"),
]
