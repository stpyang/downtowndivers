'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "start_date",
        "end_date",
        "title",
        "show_on_homepage",
    )
