# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0011_braintreeresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='braintreetransaction',
            name='braintree_id',
            field=models.CharField(max_length=30, serialize=False, editable=False, primary_key=True),
        ),
    ]
