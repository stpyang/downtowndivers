# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0016_auto_20180715_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='fill',
            name='other_cost',
            field=models.DecimalField(editable=False, default=Decimal('0.00'), decimal_places=2, max_digits=20, verbose_name='Oxygen Cost'),
        ),
        migrations.AddField(
            model_name='fill',
            name='other_price',
            field=models.FloatField(editable=False, default=0.0, verbose_name='Other Price'),
            preserve_default=False,
        ),
    ]
