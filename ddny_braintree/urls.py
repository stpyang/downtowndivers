'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.conf.urls import url

from . import views


urlpatterns = [
    url(regex=r'^gimme_fills/$',
        view=views.gimme_fills,
        name='gimme_fills'),
    url(regex=r'^gimme_dues/$',
        view=views.gimme_dues,
        name='gimme_dues'),
]

