'''Copyright 2016 DDNY. All Rights Reserved.'''

import ast
import braintree

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.db.models import Sum
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ddny.core import cash
from ddny.views import __calculate_prepaid, oops
from fillstation.models import Fill, Prepay
from registration.models import Member, MonthlyDues
from .models import BraintreeResult


class BraintreeException(Exception):
    '''exception'''


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

            if not amount_verification == cash(amount):
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

            if braintree_result.transaction is None:
                raise BraintreeException(result.message)

            for fill in fills:
                fill.braintree_transaction_id = result.transaction.id
                fill.is_paid = True
                fill.save()
            context = {
                "amount": result.transaction.amount,
                "first_name": result.transaction.paypal_details.payer_first_name,
            }
            return render(request, "fillstation/payment_success.html", context)
        except (BraintreeException, SuspiciousOperation) as exception:
            return oops(
                request=request,
                text_template="ddny_braintree/braintree_warning.txt",
                html_template="ddny_braintree/braintree_warning.html",
                view="gimme_fills",
                error_messages=exception.args,
            )
    else:
        return oops(
            request=request,
            text_template="ddny_braintree/braintree_warning.txt",
            html_template="ddny_braintree/braintree_warning.html",
            view="gimme_fills",
            error_messages="Request to gimme_fills must be of method POST",
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
            username = request.POST.get("member")
            member = Member.objects.get(username=username)

            # Double check that we priced the fillz correctly
            amount_verification = int(months) * settings.MONTHLY_DUES

            if not amount_verification == cash(amount):
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

            if braintree_result.transaction is None:
                raise BraintreeException(result.message)

            MonthlyDues.objects.create(
                member=member,
                months=months,
                braintree_transaction_id=result.transaction.id,
                is_paid=True,
            )

            context = {
                "amount": result.transaction.amount,
                "first_name": result.transaction.paypal_details.payer_first_name,
            }
            return render(request, "fillstation/payment_success.html", context)
        except (BraintreeException, SuspiciousOperation) as exception:
            return oops(
                request=request,
                text_template="ddny_braintree/braintree_warning.txt",
                html_template="ddny_braintree/braintree_warning.html",
                view="gimme_dues",
                error_messages=exception.args,
            )
    else:
        return oops(
            request=request,
            text_template="ddny_braintree/braintree_warning.txt",
            html_template="ddny_braintree/braintree_warning.html",
            view="gimme_fills",
            error_messages="Request to gimme_fills must be of method POST",
        )


@csrf_exempt
def gimme_prepay(request):
    '''Braintree fills'''
    if request.method == "POST":
        try:
            nonce = request.POST.get("payment_method_nonce")
            amount = request.POST.get("amount")
            description = request.POST.get("description")
            username = request.POST.get("member")
            member = Member.objects.get(username=username)
            amount = cash(amount)

            # Verification passed, let's submit the transaction
            result = braintree.Transaction.sale({
                "amount": amount,
                "payment_method_nonce": nonce,
                "options": {
                    "paypal": {
                        "description": description,
                    },
                    "submit_for_settlement": True,
                },
            })
            braintree_result = BraintreeResult.objects.parse(result)

            if braintree_result.transaction is None:
                raise BraintreeException(result.message)

            prepaid_balance = __calculate_prepaid(member) + amount
            # first pay for existing fills
            for fill in Fill.objects.unpaid().filter(bill_to__username=username):
                if prepaid_balance >= fill.total_price:
                    fill.braintree_transaction_id = result.transaction.id
                    fill.is_paid = True
                    fill.save()
                    Prepay.objects.create(
                        member=member,
                        amount=-fill.total_price,
                        fill=fill,
                        is_paid=True,
                    )
                    prepaid_balance = prepaid_balance - fill.total_price

            Prepay.objects.create(
                member=Member.objects.get(username=username),
                amount=amount,
                braintree_transaction_id=result.transaction.id,
                is_paid=True,
            )

            context = {
                "amount": result.transaction.amount,
                "first_name": result.transaction.paypal_details.payer_first_name,
            }
            return render(request, "fillstation/payment_success.html", context)
        except (BraintreeException, SuspiciousOperation) as exception:
            return oops(
                request=request,
                text_template="ddny_braintree/braintree_warning.txt",
                html_template="ddny_braintree/braintree_warning.html",
                view="gimme_dues",
                error_messages=exception.args,
            )
    return oops(
        request=request,
        text_template="ddny_braintree/braintree_warning.txt",
        html_template="ddny_braintree/braintree_warning.html",
        view="gimme_fills",
        error_messages="Request to gimme_prepay must be of method POST",
    )
