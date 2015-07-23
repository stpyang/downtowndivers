# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0005_auto_20150827_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill',
            name='air_cost',
            field=models.DecimalField(max_digits=20, verbose_name='Air Cost', decimal_places=2, editable=False, default=Decimal('0.03')),
        ),
        migrations.AlterField(
            model_name='fill',
            name='equipment_cost',
            field=models.DecimalField(max_digits=20, verbose_name='Equipment Cost', decimal_places=2, editable=False, default=Decimal('0.10')),
        ),
        migrations.AlterField(
            model_name='fill',
            name='oxygen_cost',
            field=models.DecimalField(max_digits=20, verbose_name='Oxygen Cost', decimal_places=2, editable=False, default=Decimal('0.20')),
        ),
    ]
