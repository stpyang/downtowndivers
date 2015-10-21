# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0014_braintreetransaction_paypal_fees'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='braintreetransaction',
            name='paypal_fees',
        ),
    ]
