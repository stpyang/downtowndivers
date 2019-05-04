'''Copyright 2016 DDNY. All Rights Reserved.'''

from debug import views

from django.conf import settings
from django.urls import path


urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path('todo/',
            view=views.todo,
            name='todo'),
        path('blend_tests/',
            view=views.blend_tests,
            name='blend_tests'),
        path('fill_tests/',
            view=views.fill_tests,
            name='fill_tests'),
    ]
