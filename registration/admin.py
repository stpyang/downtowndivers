'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.contrib import admin

from .models import ConsentA, Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    ''' admin class for Specification model '''
    fieldsets = (
        ("User", {
            "fields": (
                "user",
                "gender",
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
    )
    list_display = ("user",) + Member.member_info_fields


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
