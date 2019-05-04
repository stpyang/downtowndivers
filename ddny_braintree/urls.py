'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.urls import path

from . import views


urlpatterns = [
    path('gimme_dues/',
        view=views.gimme_dues,
        name='gimme_dues'),
    path('gimme_fills/',
        view=views.gimme_fills,
        name='gimme_fills'),
    path('gimme_prepay/',
        view=views.gimme_prepay,
        name='gimme_prepay'),
]

