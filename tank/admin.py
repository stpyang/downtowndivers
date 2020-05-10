'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.contrib.admin import register, ModelAdmin, TabularInline

from .models import Hydro, Specification, Tank, Vip


class HydroInline(TabularInline):
    '''
    https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#django.contrib.admin.TabularInline
    '''

    model = Hydro
    extra = 0


class VipInline(TabularInline):
    '''
    https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#django.contrib.admin.TabularInline
    '''

    model = Vip
    extra = 0


@register(Specification)
class SpecificationAdmin(ModelAdmin):
    '''https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#modeladmin-objects'''

    fieldsets = (
        ('Name', {
            'fields': ('name',),
        }),
        ('Material', {
            'fields': ('material',),
        }),
        ('Volume (ft^3)', {
            'fields': ('volume',),
        }),
        ('Pressure (psi)', {
            'fields': ('working_pressure',),
        }),
    )
    list_display = ('name', 'slug', 'material', 'volume', 'working_pressure')


@register(Tank)
class TankAdmin(ModelAdmin):
    '''https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#modeladmin-objects'''

    fieldsets = (
        ('Serial Number and Tank Codes', {
            'fields': ('serial_number', 'code', 'doubles_code'),
        }),
        ('Owner', {
            'fields': ('owner',),
        }),
        ('Specification', {
            'fields': ('spec',),
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )
    list_display = (
        'code',
        'doubles_code',
        'serial_number',
        'spec',
        'owner',
        'is_active',
        'last_hydro',
        'last_vip'
    )
    inlines = [HydroInline, VipInline]


@register(Vip)
class VipAdmin(ModelAdmin):
    '''https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#modeladmin-objects'''

    fieldsets = (
        ('Header', {
            'fields': Vip.header_fields,
        }),
        ('Address', {
            'fields': Vip.address_fields,
        }),
        ('Tank', {
            'fields': Vip.tank_fields,
        }),
        ('External', {
            'fields': Vip.external_fields,
        }),
        ('Internal', {
            'fields': Vip.internal_fields,
        }),
        ('Threads', {
            'fields': Vip.threads_fields,
        }),
        ('Valve', {
            'fields': Vip.valve_fields,
        }),
        ('Cylinder Condition', {
            'fields': Vip.cylindercondition_fields,
        }),
        ('Inspector', {
            'fields': Vip.inspector_fields,
        }),
    )
    list_display = ('id',) + Vip.header_fields + Vip.inspector_fields
