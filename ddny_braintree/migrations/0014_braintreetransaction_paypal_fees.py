# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0013_auto_20150916_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='braintreetransaction',
            name='paypal_fees',
            field=models.DecimalField(verbose_name='Paypal Fees', editable=False, default=Decimal('0'), max_digits=20, decimal_places=2),
        ),
    ]
