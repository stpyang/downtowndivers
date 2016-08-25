# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0012_prepay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill',
            name='argon_cost',
            field=models.DecimalField(max_digits=20, editable=False, default=Decimal('1.25'), decimal_places=2, verbose_name='Argon Cost'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='helium_cost',
            field=models.DecimalField(max_digits=20, editable=False, default=Decimal('1.64'), decimal_places=2, verbose_name='Helium Cost'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='oxygen_cost',
            field=models.DecimalField(max_digits=20, editable=False, default=Decimal('0.35'), decimal_places=2, verbose_name='Oxygen Cost'),
        ),
    ]
