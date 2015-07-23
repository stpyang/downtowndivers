# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0001_squashed_0041_auto_20150820_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill',
            name='air_cost',
            field=models.DecimalField(decimal_places=2, verbose_name='Air Cost', default=Decimal('0.0299999999999999988897769753748434595763683319091796875'), editable=False, max_digits=20),
        ),
        migrations.AlterField(
            model_name='fill',
            name='equipment_cost',
            field=models.DecimalField(decimal_places=2, verbose_name='Equipment Cost', default=Decimal('0.1000000000000000055511151231257827021181583404541015625'), editable=False, max_digits=20),
        ),
        migrations.AlterField(
            model_name='fill',
            name='helium_cost',
            field=models.DecimalField(decimal_places=2, verbose_name='Helium Cost', default=Decimal('2'), editable=False, max_digits=20),
        ),
    ]
