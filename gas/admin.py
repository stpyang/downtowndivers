'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.contrib.admin import register, ModelAdmin

from .models import Gas


@register(Gas)
class GasAdmin(ModelAdmin):
    '''https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#modeladmin-objects'''

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
                "other_percentage",
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
        "other_percentage",
        "cost",
    )
