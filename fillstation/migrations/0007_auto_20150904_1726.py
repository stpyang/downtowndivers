# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0006_auto_20150827_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill',
            name='braintree_transaction_id',
            field=models.CharField(verbose_name='Braintree', editable=False, max_length=30, default=''),
        ),
    ]
