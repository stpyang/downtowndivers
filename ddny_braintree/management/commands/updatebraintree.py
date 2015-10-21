'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.core.management.base import BaseCommand, CommandError
from fillstation.models import Fill
from registration.models import MonthlyDues
from ddny_braintree.models import BraintreeTransaction
import braintree


# A list of transactions to exclude since they are in their final state
FINAL_STATE = [
    "failed",
    "voided",
    "settled",
]

class Command(BaseCommand):
    help = 'Update status on BraintreeTransactions and associated fills'

    def handle(self, *args, **options):
        for t in BraintreeTransaction.objects.exclude(status__in=FINAL_STATE):
            transaction = braintree.Transaction.find(t.braintree_id)
            print("Transaction " + transaction.id + " " + transaction.status)
            t.paypal_fees = transaction.paypal_details.transaction_fee_amount
            t.status = transaction.status
            t.save()
            for f in Fill.objects.filter(braintree_transaction_id=transaction.id):
                f.is_paid = t.status == "settled" or t.status == "settling"
                f.save()
            for d in MonthlyDues.objects.filter(braintree_transaction_id=transaction.id):
                d.is_paid = t.status == "settled" or t.status == "settling"
                d.save()
