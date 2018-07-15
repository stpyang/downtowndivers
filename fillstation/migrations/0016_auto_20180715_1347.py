# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0015_auto_20180715_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill',
            name='DEPRECATED_equipment_cost',
            field=models.DecimalField(editable=False, max_digits=20, default=Decimal('0.00'), decimal_places=2, verbose_name='[DEPRECATED] Equipment Cost'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='DEPRECATED_equipment_price',
            field=models.FloatField(editable=False, default=Decimal('0.00'), verbose_name='[DEPRECATED] Equipment Price'),
        ),
    ]
