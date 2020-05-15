'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.conf import settings
from django.urls import path

from debug import views


urlpatterns = []  # pylint: disable=invalid-name

if settings.DEBUG:
    urlpatterns += [
        path('blend_tests/',
             view=views.blend_tests,
             name='blend_tests'),
        path('fill_tests/',
             view=views.fill_tests,
             name='fill_tests'),
    ]
