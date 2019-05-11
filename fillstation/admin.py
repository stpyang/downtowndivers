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
                "is_equipment_surcharge",
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
                "equipment_surcharge_key",
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
        ("Cost (per cubic foot)", {
            "fields": (
                "air_cost",
                "argon_cost",
                "helium_cost",
                "oxygen_cost",
                "equipment_cost_proportional",
            ),
            "description": "Cost per cubic foot.",
        }),
        ("Price", {
            "fields": (
                "air_price",
                "argon_price",
                "helium_price",
                "oxygen_price",
                "equipment_price_proportional",
                "total_price",
            ),
        }),
    )
    list_display = (
        "id",
        "is_paid",
        "is_equipment_surcharge",
        "datetime",
        "blender",
        "equipment_surcharge_key",
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
        "air_cost",
        "argon_cost",
        "helium_cost",
        "oxygen_cost",
        "equipment_cost_proportional",
        "equipment_price_proportional",
        "air_price",
        "argon_price",
        "helium_price",
        "oxygen_price",
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
