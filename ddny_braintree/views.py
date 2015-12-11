'''Copyright 2016 DDNY. All Rights Reserved.'''

import ast
import braintree
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.db.models import Sum
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ddny.views import oops
from fillstation.models import Fill

from .models import BraintreeResult
from registration.models import Member, MonthlyDues


class BraintreeException(Exception):
    pass


@csrf_exempt
def gimme_fills(request):
    '''Braintree dues'''
    if request.method == "POST":
        try:
            nonce = request.POST.get("payment_method_nonce")
            amount = request.POST.get("amount")
            description = request.POST.get("description")
            fillz = request.POST.get("fillz")
            fills = Fill.objects.filter(id__in=ast.literal_eval(fillz))

            # Double check that we priced the fillz correctly
            amount_verification = fills.aggregate(Sum('total_price'))
            amount_verification = amount_verification['total_price__sum']

            if not amount_verification == Decimal(amount).quantize(settings.PENNY):
                raise SuspiciousOperation(
                    "Payment amount verification failure. ({0} != {1})".format(
                        amount_verification, amount
                    )
                )

            # Verification passed, let's submit the transaction
            result = braintree.Transaction.sale({
                "amount": amount,
                "payment_method_nonce": nonce,
                "custom_fields": {
                    "fillz": fillz,
                },
                "options": {
                    "paypal": {
                        "description": description,
                    },
                    "submit_for_settlement": True,
                },
            })
            braintree_result = BraintreeResult.objects.parse(result)

            if not braintree_result.is_success:
                raise BraintreeException(result.message)

            for f in fills:
                f.braintree_transaction_id = result.transaction.id
                f.is_paid = True
                f.save()
            context = {
                "amount": result.transaction.amount,
                "first_name": result.transaction.paypal_details.payer_first_name,
            }
            return render(request, "fillstation/payment_success.html", context)
        except (BraintreeException, SuspiciousOperation) as e:
            return oops(
                request=request,
                text_template="ddny_braintree/braintree_warning.txt",
                html_template="ddny_braintree/braintree_warning.html",
                view="gimme_fills",
                error_messages=e.args,
            )


@csrf_exempt
def gimme_dues(request):
    '''Braintree fills'''
    if request.method == "POST":
        try:
            nonce = request.POST.get("payment_method_nonce")
            amount = request.POST.get("amount")
            description = request.POST.get("description")
            months = request.POST.get("months")
            member = request.POST.get("member")

            # Double check that we priced the fillz correctly
            amount_verification = int(months) * settings.MONTHLY_DUES

            if not amount_verification == Decimal(amount).quantize(settings.PENNY):
                raise SuspiciousOperation(
                    "Payment amount verification failure. ({0} != {1})".format(
                        amount_verification, amount
                    )
                )

            # Verification passed, let's submit the transaction
            result = braintree.Transaction.sale({
                "amount": amount,
                "payment_method_nonce": nonce,
                "custom_fields": {
                    "months": months,
                },
                "options": {
                    "paypal": {
                        "description": description,
                    },
                    "submit_for_settlement": True,
                },
            })
            braintree_result = BraintreeResult.objects.parse(result)

            if not braintree_result.is_success:
                raise BraintreeException(result.message)

            MonthlyDues.objects.create(
                member=Member.objects.get(username=member),
                months=months,
                braintree_transaction_id=result.transaction.id,
                is_paid=True,
            )

            context = {
                "amount": result.transaction.amount,
                "first_name": result.transaction.paypal_details.payer_first_name,
            }
            return render(request, "fillstation/payment_success.html", context)
        except (BraintreeException, SuspiciousOperation) as e:
            return oops(
                request=request,
                text_template="ddny_braintree/braintree_warning.txt",
                html_template="ddny_braintree/braintree_warning.html",
                view="gimme_dues",
                error_messages=e.args,
            )
