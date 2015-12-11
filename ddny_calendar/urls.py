'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.conf.urls import url

from . import views


urlpatterns = [
    url(regex=r'^add_event/$',
        view=views.add_event,
        name='add_event'),
    url(regex=r'^delete_event/$',
        view=views.delete_event,
        name='delete_event'),
    url(regex=r'^update_event/$',
        view=views.update_event,
        name='update_event'),
    url(regex=r'^feed.ics/$',
        view=views.EventFeed(),
        name='feed'),
]
