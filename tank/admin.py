'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.contrib import admin

from .models import Hydro, Specification, Tank, Vip


class HydroInline(admin.TabularInline):
    model = Hydro
    extra = 0


class VipInline(admin.TabularInline):
    model = Vip
    extra = 0


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    ''' admin class for Specification model '''
    fieldsets = (
        ("Name", {
            "fields": ("name",),
        }),
        ("Metal", {
            "fields": ("metal",),
        }),
        ("Volume (ft^3)", {
            "fields": ("volume",),
        }),
        ("Pressure (psi)", {
            "fields": ("pressure",),
        }),
    )
    list_display = ("name", "slug", "metal", "volume", "pressure")


@admin.register(Tank)
class TankAdmin(admin.ModelAdmin):
    ''' admin class for Tank model '''
    fieldsets = (
        ("Serial Number and Tank Codes", {
            "fields": ("serial_number", "code", "doubles_code"),
        }),
        ("Owner", {
            "fields": ("owner",),
        }),
        ("Specification", {
            "fields": ("spec",),
        }),
        ("Status", {
            "fields": ("is_active",),
        }),
    )
    list_display = (
        "code",
        "doubles_code",
        "serial_number",
        "spec",
        "owner",
        "is_active",
        "last_hydro",
        "last_vip"
    )
    inlines = [HydroInline, VipInline]
