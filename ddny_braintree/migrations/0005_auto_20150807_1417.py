# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0004_auto_20150807_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='braintreepaypaldetails',
            name='braintree_transaction',
            field=models.OneToOneField(to='ddny_braintree.BraintreeTransaction', on_delete=models.CASCADE),
        ),
    ]
