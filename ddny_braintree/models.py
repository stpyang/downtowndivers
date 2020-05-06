'''Copyright 2016 DDNY. All Rights Reserved.'''


from django.db import models
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel

from ddny.core import cash


class BraintreeTransactionMixin(models.Model):
    '''Braintree transactions for fills and dues'''

    class Meta:
        '''https://docs.djangoproject.com/en/2.2/ref/models/options/#model-meta-options'''
        abstract = True

    braintree_transaction_id = models.CharField(
        default="",
        editable=False,
        max_length=30,
        verbose_name="Braintree"
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name="Is Paid",
    )


class BraintreeResultManager(models.Manager):  # pylint: disable=too-few-public-methods
    '''https://docs.djangoproject.com/en/2.2/topics/db/managers/'''

    def parse(self, result):
        '''parse a POST result into a BraintreeTransaction object'''
        if result.transaction is not None:
            transaction = BraintreeTransaction.objects.parse(result.transaction)
            result = self.create(transaction=transaction)
            result.save()
            return result
        error = BraintreeError.objects.parse(result)
        result = self.create(error=error)
        result.save()
        return result


class BraintreeResult(TimeStampedModel):
    '''https://developers.braintreepayments.com/\
            javascript+python/reference/general/result-objects'''

    objects = BraintreeResultManager()

    # NOTE(stpyang): leave the one-to-one fields in quotes so that we avoid
    # circular dependencies
    transaction = models.OneToOneField(
        "BraintreeTransaction",
        null=True,
        on_delete=models.CASCADE,
    )
    error = models.OneToOneField(
        "BraintreeError",
        null=True,
        on_delete=models.CASCADE,
    )


class BraintreeTransactionManager(models.Manager):  # pylint: disable=too-few-public-methods
    '''https://docs.djangoproject.com/en/2.2/topics/db/managers/'''

    def parse(self, result):
        '''parse a POST result into a BraintreeTransaction object'''
        transaction = self.create(
            braintree_id=result.id,
            amount=result.amount,
            status=result.status,
        )
        if result.paypal_details:
            paypal_details = BraintreePaypalDetails.objects.parse(
                result=result.paypal_details,
                braintree_transaction=transaction,
            )
            paypal_details.save()
        return transaction


class BraintreeTransaction(TimeStampedModel):
    '''https://developers.braintreepayments.com/\
            javascript+python/reference/response/transaction'''

    class Meta:
        '''https://docs.djangoproject.com/en/2.2/ref/models/options/#model-meta-options'''
        verbose_name = "Transaction"
        ordering = ("-created",)

    STATUS = Choices(
        "authorized",
        "authorization expired",
        "processor declined",
        "gateway rejected",
        "failed",
        "voided",
        "submitted for settlement",
        "settling",
        "settled",
        "settlement declined",
        "settlement pending",
        "",
    )

    objects = BraintreeTransactionManager()

    braintree_id = models.CharField(
        editable=False,
        max_length=30,
        primary_key=True,
    )
    amount = models.DecimalField(
        decimal_places=2,
        default=cash(0),
        editable=False,
        max_digits=20,
        verbose_name="Amount",
    )
    status = StatusField(
        default="",
        db_index=True,
        verbose_name="Status",
    )
    status_changed = MonitorField(monitor='status')

    @property
    def is_paid(self):
        '''self explanatory'''
        return self.status == "settled" or self.status == "settling"


class BraintreePaypalDetailsManager(models.Manager):  # pylint: disable=too-few-public-methods
    '''https://docs.djangoproject.com/en/2.2/topics/db/managers/'''

    def parse(self, result, braintree_transaction=None):
        '''parse paypal details from POST data'''
        return self.create(
            image_url=result.image_url,
            payer_email=result.payer_email,
            payer_first_name=result.payer_first_name,
            payer_last_name=result.payer_last_name,
            payment_id=result.payment_id,
            transaction_fee_amount=result.transaction_fee_amount,
            braintree_transaction=braintree_transaction,
        )


class BraintreePaypalDetails(TimeStampedModel):
    '''https://developers.braintreepayments.com/\
            javascript+python/reference/response/transaction#paypal_details'''

    class Meta:
        '''https://docs.djangoproject.com/en/2.2/ref/models/options/#model-meta-options'''
        verbose_name_plural = "Braintree Paypal Details"

    objects = BraintreePaypalDetailsManager()

    image_url = models.URLField(
        editable=False,
        null=True,
        verbose_name="Image",
    )
    payer_email = models.EmailField(
        editable=False,
        null=True,
        verbose_name="Paypal e-mail",
    )
    payer_first_name = models.CharField(
        default="",
        editable=False,
        max_length=30,
        verbose_name="First Name",
    )
    payer_last_name = models.CharField(
        default="",
        editable=False,
        max_length=30,
        verbose_name="Last Name",
    )
    payment_id = models.CharField(
        default="",
        editable=False,
        max_length=30,
        verbose_name="Payment Id",
    )
    transaction_fee_amount = models.DecimalField(
        decimal_places=2,
        default=cash(0.00),
        editable=False,
        max_digits=6,
        verbose_name="Transaction Fee",
    )
    braintree_transaction = models.OneToOneField(
        BraintreeTransaction,
        related_name="paypal_details",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.payer_email


class BraintreeErrorManager(models.Manager):  # pylint: disable=too-few-public-methods
    '''https://docs.djangoproject.com/en/2.2/topics/db/managers/'''

    def parse(self, result):
        '''parse a POST result into a BraintreeError object'''
        return self.create(
            message=result.message,
            params=str(result.params)[0:255]
        )


class BraintreeError(TimeStampedModel):
    '''https://developers.braintreepayments.com/\
            javascript+python/reference/general/result-objects#error-results'''

    class Meta:
        '''https://docs.djangoproject.com/en/2.2/ref/models/options/#model-meta-options'''
        verbose_name = "Error"

    objects = BraintreeErrorManager()
    message = models.CharField(
        editable=False,
        max_length=255,
    )
    params = models.CharField(
        editable=False,
        max_length=255,
    )
