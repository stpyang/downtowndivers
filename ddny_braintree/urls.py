'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.conf.urls import url

from . import views


urlpatterns = [
    url(regex=r'^gimme/$',
        view=views.gimme,
        name='gimme'),
]

