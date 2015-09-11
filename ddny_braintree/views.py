'''Copyright 2015 DDNY. All Rights Reserved.'''

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


class BraintreeException(Exception):
    pass


@csrf_exempt
def gimme(request):
    ''' Braintree stuff '''
    if request.method == "POST":
        try:
            nonce = request.POST.get("payment_method_nonce")
            amount = request.POST.get("amount")
            fillz = request.POST.get("fillz")
            fills = Fill.objects.filter(id__in=ast.literal_eval(fillz))

            # Double check that we priced the fillz correctly
            amount_verification = fills.aggregate(Sum('total_price'))
            amount_verification = amount_verification['total_price__sum']

            # Verification passed, let's submit the transaction
            result = braintree.Transaction.sale({
                "amount": amount,
                "payment_method_nonce": nonce,
                "custom_fields": {
                    "fillz": fillz,
                },
                "options": {
                    "submit_for_settlement": True,
                },
            })
            braintree_result = BraintreeResult.objects.parse(result)

            if not amount_verification == Decimal(amount).quantize(settings.PENNY):
                raise SuspiciousOperation(
                    "Payment amount verification failure. ({0} != {1})".format(
                        amount_verification, amount
                    )
                )
            if not braintree_result.is_success:
                raise BraintreeException(result.message)

            for f in fills:
                f.braintree_transaction_id = result.transaction.id
                f.is_paid = True
                f.save()
            context = {
                "amount": result.transaction.amount,
                "first_name": result.transaction.paypal_details.payer_first_name,
                "last_name": result.transaction.paypal_details.payer_last_name,
            }
            return render(request, "fillstation/payment_success.html", context)
        except (BraintreeException, SuspiciousOperation) as e:
            return oops(
                request=request,
                text_template="ddny_braintree/braintree_warning.txt",
                html_template="ddny_braintree/braintree_warning.html",
                view="gimme",
                error_messages=e.args,
            )
