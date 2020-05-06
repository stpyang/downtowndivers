'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.contrib import admin

from .models import BraintreeError, BraintreeTransaction, BraintreePaypalDetails


class BraintreePaypalDetailsInline(admin.TabularInline):
    '''https://docs.djangoproject.com/en/2.2/ref/contrib/admin/
       #django.contrib.admin.TabularInline'''
    model = BraintreePaypalDetails
    extra = 0
    readonly_fields = (
        "id",
        "payer_email",
        "payer_first_name",
        "payer_last_name",
        "payment_id",
        "transaction_fee_amount",
    )


@admin.register(BraintreeTransaction)
class BraintreeTransactionAdmin(admin.ModelAdmin):
    '''admin class for Braintree transactions'''
    fieldsets = (
        ("Info", {
            "fields": (
                "braintree_id",
                "status",
                "amount",
                "is_paid",
            )
        }),
    )
    readonly_fields = (
        "status",
        "braintree_id",
        "amount",
        "is_paid",
    )
    list_display = (
        "is_paid",
        "created",
        "braintree_id",
        "amount",
        "status",
        "status_changed",
        "paypal_details",
    )
    inlines = [BraintreePaypalDetailsInline]


@admin.register(BraintreeError)
class BraintreeErrorAdmin(admin.ModelAdmin):
    '''admin class for Braintree errors.  may there always be none.'''
    fieldsets = (
        ("Error", {
            "fields": (
                "message",
                "params",
            )
        }),
    )
    readonly_fields = (
        "message",
        "params",
    )
    list_display = (
        "created",
        "message",
        "params",
    )
