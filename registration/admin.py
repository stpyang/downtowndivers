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
            "fields": (
                "address",
                "city",
                "state",
                "zip_code",
                "phone_number",
                "psi_inspector_number",
                "blender_certification",
            ),
        }),
        ("Permissions", {
            "fields": (
                "is_blender",
                "autopay_fills",
            ),
        }),
    )
    list_display = (
        "user",
        "address",
        "city",
        "state",
        "zip_code",
        "phone_number",
        "psi_inspector_number",
        "blender_certification",
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
            "fields": ConsentA.boolean_fields,
        }),
        ("Signatures", {
            "fields": ConsentA.signature_fields,
        }),
    )
