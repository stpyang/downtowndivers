'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.conf.urls import url

from . import views


urlpatterns = [
    url(regex=r'^blend/$',
        view=views.blend,
        name='blend'),
    url(regex=r'^download/$',
        view=views.download,
        name='download'),
    url(regex=r'^fill/$',
        view=views.fill,
        name='fill'),
    url(regex=r'^log/$',
        view=views.FillLog.as_view(),
        name='log'),
    url(regex=r'^log_fill/$',
        view=views.log_fill,
        name='log_fill'),
    url(regex=r'^pay_fills/(?P<slug>\w+)/$',
        view=views.PayFills.as_view(),
        name='pay_fills'),
]
