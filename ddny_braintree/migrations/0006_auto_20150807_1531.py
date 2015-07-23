# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0005_auto_20150807_1417'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='braintreepaypaldetails',
            options={'verbose_name_plural': 'Braintree Paypal Details'},
        ),
    ]
