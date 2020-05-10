'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.contrib.admin import ModelAdmin, register

from .models import ConsentA, Member, MonthlyDues


@register(Member)
class MemberAdmin(ModelAdmin):
    '''https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#modeladmin-objects'''

    fieldsets = (
        ('User', {
            'fields': (
                'user',
                'gender',
                'member_since',
            ),
        }),
        ('Address', {
            'fields': Member.address_fields,
        }),
        ('Permissions', {
            'fields': (
                'is_blender',
                'autopay_fills',
                'is_treasurer',
                'honorary_member',
            ),
        }),
    )
    list_display = (
        'user',
        'member_since',
        'last_login',
        'psi_inspector_number',
        'blender_certification'
    ) + Member.address_fields


@register(ConsentA)
class ConsentAAdmin(ModelAdmin):
    '''https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#modeladmin-objects'''

    fieldsets = (
        ('Header', {
            'fields': ('member', ),
        }),
        ('Consents', {
            'fields': ConsentA.boolean_fields,
        }),
        ('Signatures', {
            'fields': ConsentA.signature_fields,
        }),
    )


@register(MonthlyDues)
class MonthlyDuesAdmin(ModelAdmin):
    '''https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#modeladmin-objects'''

    fieldsets = (
        ('Dues', {
            'fields': (
                'member',
                'months',
            ),
        }),
    )
    list_display = ('member', 'months', 'braintree_transaction_id', )
