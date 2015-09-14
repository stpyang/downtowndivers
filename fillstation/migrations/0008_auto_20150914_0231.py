# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0007_auto_20150904_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill',
            name='helium_cost',
            field=models.DecimalField(verbose_name='Helium Cost', decimal_places=2, default=Decimal('1.35'), editable=False, max_digits=20),
        ),
    ]
