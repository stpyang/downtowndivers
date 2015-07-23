# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BraintreeCustomerDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('email', models.EmailField(null=True, max_length=254)),
                ('first_name', models.CharField(default='', max_length=30)),
                ('last_name', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='BraintreePaypalDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('image_url', models.URLField(null=True)),
                ('payer_email', models.EmailField(null=True, max_length=254)),
                ('payer_first_name', models.CharField(default='', max_length=30)),
                ('payer_last_name', models.CharField(default='', max_length=30)),
                ('payment_id', models.CharField(default='', max_length=30)),
                ('transaction_fee_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='BraintreeTransaction',
            fields=[
                ('braintree_id', models.CharField(primary_key=True, serialize=False, max_length=6)),
                ('amount', models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0'), editable=False, verbose_name='Amount')),
                ('status', models.CharField(verbose_name='Status', default='', choices=[('authorized', 'authorized'), ('authorization expired', 'authorization expired'), ('processor declined', 'processor declined'), ('gateway rejected', 'gateway rejected'), ('failed', 'failed'), ('voided', 'voided'), ('submitted for settlement', 'submitted for settlement'), ('settling', 'settling'), ('settled', 'settled'), ('settlement declined', 'settlement declined'), ('settlement pending', 'settlement pending')], max_length=17)),
                ('customer_details', models.ForeignKey(to='ddny_braintree.BraintreeCustomerDetails', null=True)),
                ('paypal_details', models.ForeignKey(to='ddny_braintree.BraintreePaypalDetails', null=True)),
            ],
        ),
    ]
