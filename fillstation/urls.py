'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.urls import path

from . import views


urlpatterns = [  # pylint: disable=invalid-name
    path('blend/',
         view=views.blend,
         name='blend'),
    path('download/',
         view=views.download,
         name='download'),
    path('fill/',
         view=views.fill,
         name='fill'),
    path('log/',
         view=views.FillLog.as_view(),
         name='log'),
    path('log_fill/',
         view=views.log_fill,
         name='log_fill'),
    path('prepay/',
         view=views.prepay,
         name='prepay'),
    path('unpaid_fills/<slug:slug>/',
         view=views.UnpaidFills.as_view(),
         name='unpaid_fills'),
]
