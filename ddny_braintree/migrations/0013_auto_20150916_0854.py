# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0012_auto_20150904_1710'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='braintreetransaction',
            options={'verbose_name': 'Transaction', 'ordering': ('-created',)},
        ),
        migrations.AlterField(
            model_name='braintreepaypaldetails',
            name='braintree_transaction',
            field=models.OneToOneField(related_name='paypal_details', to='ddny_braintree.BraintreeTransaction', on_delete=models.CASCADE),
        ),
    ]
