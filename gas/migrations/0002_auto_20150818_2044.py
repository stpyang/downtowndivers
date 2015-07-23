# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('gas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gas',
            name='argon_percentage',
            field=models.DecimalField(decimal_places=1, default=Decimal('0'), max_digits=5, verbose_name='Percentage Argon'),
        ),
        migrations.AlterField(
            model_name='gas',
            name='helium_percentage',
            field=models.DecimalField(decimal_places=1, default=Decimal('0'), max_digits=5, verbose_name='Percentage Helium'),
        ),
        migrations.AlterField(
            model_name='gas',
            name='oxygen_percentage',
            field=models.DecimalField(decimal_places=1, default=Decimal('0'), max_digits=5, verbose_name='Percentage Oxygen'),
        ),
    ]
