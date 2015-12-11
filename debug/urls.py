'''Copyright 2016 DDNY. All Rights Reserved.'''

from debug import views

from django.conf import settings
from django.conf.urls import url


urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        url(regex=r'^todo/$',
            view=views.todo,
            name='todo'),
        url(regex=r'^blend_tests/$',
            view=views.blend_tests,
            name='blend_tests'),
        url(regex=r'^fill_tests/$',
            view=views.fill_tests,
            name='fill_tests'),
    ]
