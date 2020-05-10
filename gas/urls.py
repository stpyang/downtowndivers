'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.urls import path

from . import views


urlpatterns = [  # pylint: disable=invalid-name
    path('<slug:slug>/',
         view=views.GasDetail.as_view(),
         name='detail'),
    path('',
         view=views.GasList.as_view(),
         name='list'),
]
