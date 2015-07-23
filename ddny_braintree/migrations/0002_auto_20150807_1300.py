# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='braintreetransaction',
            name='customer_details',
        ),
        migrations.AlterField(
            model_name='braintreetransaction',
            name='braintree_id',
            field=models.CharField(max_length=6, editable=False, primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='BraintreeCustomerDetails',
        ),
    ]
