# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0002_auto_20150807_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='braintreetransaction',
            name='paypal_details',
        ),
        migrations.AddField(
            model_name='braintreepaypaldetails',
            name='braintree_transaction',
            field=models.ForeignKey(to='ddny_braintree.BraintreeTransaction', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='braintreepaypaldetails',
            name='image_url',
            field=models.URLField(verbose_name='Image', editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='braintreepaypaldetails',
            name='payer_email',
            field=models.EmailField(verbose_name='Paypal e-mail', max_length=254, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='braintreepaypaldetails',
            name='payer_first_name',
            field=models.CharField(verbose_name='First Name', max_length=30, editable=False, default=''),
        ),
        migrations.AlterField(
            model_name='braintreepaypaldetails',
            name='payer_last_name',
            field=models.CharField(verbose_name='Last Name', max_length=30, editable=False, default=''),
        ),
        migrations.AlterField(
            model_name='braintreepaypaldetails',
            name='payment_id',
            field=models.CharField(verbose_name='Payment Id', max_length=30, editable=False, default=''),
        ),
        migrations.AlterField(
            model_name='braintreepaypaldetails',
            name='transaction_fee_amount',
            field=models.DecimalField(verbose_name='Transaction Fee', max_digits=6, editable=False, decimal_places=2, default=Decimal('0')),
        ),
    ]
