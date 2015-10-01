'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.contrib import admin

from .models import ConsentA, Member, MonthlyDues


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    ''' admin class for Specification model '''
    fieldsets = (
        ("User", {
            "fields": (
                "user",
                "gender",
                "member_since",
            ),
        }),
        ("Info", {
            "fields": Member.member_info_fields,
        }),
        ("Permissions", {
            "fields": (
                "is_blender",
                "autopay_fills",
            ),
        }),
        ("Dues", {
            "fields": (
                "monthly_dues_start_date",
            ),
        }),
    )
    list_display = ("user", "member_since") + Member.member_info_fields


@admin.register(ConsentA)
class ConsentAAdmin(admin.ModelAdmin):
    ''' admin class for Specification model '''
    fieldsets = (
        ("Header", {
            "fields": (
                "member",
            ),
        }),
        ("Consents", {
            "fields": ConsentA.boolean_fields,
        }),
        ("Signatures", {
            "fields": ConsentA.signature_fields,
        }),
    )


@admin.register(MonthlyDues)
class MonthlyDuesAdmin(admin.ModelAdmin):
    ''' admin class for Specification model '''
    fieldsets = (
        ("Dues", {
            "fields": (
                "member",
                "months",
                "is_paid",
            ),
        }),
    )
    list_display = ("member", "months", "braintree_transaction_id", "is_paid", )
