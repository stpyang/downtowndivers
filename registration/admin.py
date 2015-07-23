'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.contrib import admin

from .models import ConsentA, Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    ''' admin class for Specification model '''
    fieldsets = (
        ("User", {
            "fields": ("user",),
        }),
        ("Permissions", {
            "fields": (
                "is_blender",
                "autopay_fills"
            ),
        }),
    )
    list_display = (
        "user",
        "is_blender",
        "autopay_fills",
    )


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
            "fields": ConsentA.boolean_fields
        }),
        ("Signatures", {
            "fields": (
                "member_name",
                "member_signature",
                "member_signature_date",
                "witness_name",
                "witness_signature",
                "witness_signature_date",
            ),
        }),
    )
