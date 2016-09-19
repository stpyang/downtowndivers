'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.contrib import admin

from .models import Fill, Prepay


@admin.register(Fill)
class FillAdmin(admin.ModelAdmin):
    '''admin class for Fill model'''
    fieldsets = (
        ("Fill", {
            "fields": (
                "datetime",
                "is_paid",
                ),
            }
        ),
        ("User", {"fields": ("user",)}),
        ("Blender", {"fields": ("blender",)}),
        ("Bill To", {"fields": (
            "bill_to",)}
        ),
        ("Gas", {
            "fields": ("gas_name",),
        }),
        ("Tank", {
            "fields": (
                "tank_serial_number",
                "tank_code",
                "tank_spec",
                "tank_volume",
                "tank_working_pressure",
                "tank_factor",
            ),
        }),
        ("Psi", {
            "fields": (
                "psi_start",
                "psi_end",
                "cubic_feet",
            )}
        ),
        ("Cost", {
            "fields": (
                "equipment_cost",
                "air_cost",
                "argon_cost",
                "helium_cost",
                "oxygen_cost",
            ),
            "description": "Cost per cubic foot.",
        }),
        ("Price", {
            "fields": (
                "equipment_price",
                "air_price",
                "argon_price",
                "helium_price",
                "oxygen_price",
                "total_price",
            ),
        }),
    )
    list_display = (
        "id",
        "is_paid",
        "datetime",
        "blender",
        "bill_to",
        "tank_code",
        "gas_name",
        "psi_start",
        "psi_end",
        "total_price",
        "braintree_transaction_id",
    )
    readonly_fields = (
        "tank_serial_number",
        "tank_spec",
        "tank_volume",
        "tank_working_pressure",
        "tank_factor",
        "gas_name",
        "psi_start",
        "psi_end",
        "cubic_feet",
        "equipment_cost",
        "air_cost",
        "argon_cost",
        "helium_cost",
        "oxygen_cost",
        "equipment_price",
        "air_price",
        "argon_price",
        "helium_price",
        "oxygen_price",
        "total_price",
    )


@admin.register(Prepay)
class PrepayAdmin(admin.ModelAdmin):
    ''' admin class for Specification model '''
    fieldsets = (
        ("Prepay", {
            "fields": (
                "member",
                "amount",
                "fill",
            ),
        }),
    )
    list_display = ("member", "amount", "fill", "braintree_transaction_id")
