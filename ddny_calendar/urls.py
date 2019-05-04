'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.urls import path

from . import views


urlpatterns = [
    path('add_event/',
        view=views.add_event,
        name='add_event'),
    path('delete_event/',
        view=views.delete_event,
        name='delete_event'),
    path('update_event/',
        view=views.update_event,
        name='update_event'),
    path('feed.ics/',
        view=views.EventFeed(),
        name='feed'),
]
