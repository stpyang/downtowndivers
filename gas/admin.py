"Copyright 2015 DDNY. All Rights Reserved."

from django.contrib import admin

from .models import Gas


@admin.register(Gas)
class GasAdmin(admin.ModelAdmin):
    '''admin class for Gas model'''
    fieldsets = (
        ("Name", {
            "fields": (
                "name",
                "is_banked",
            )
        }),
        ("Composition", {
            "fields": (
                "argon_percentage",
                "helium_percentage",
                "oxygen_percentage",
            ),
            "description": "Composition of the gas in terms of base components.",
        }),
    )
    list_display = (
        "name",
        "slug",
        "is_banked",
        "argon_percentage",
        "helium_percentage",
        "oxygen_percentage",
        "cost",
    )
