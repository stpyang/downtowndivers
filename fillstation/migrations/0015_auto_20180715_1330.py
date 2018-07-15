# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0014_auto_20180714_1747'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fill',
            old_name='equipment_cost',
            new_name='DEPRECATED_equipment_cost',
        ),
        migrations.RenameField(
            model_name='fill',
            old_name='equipment_price',
            new_name='DEPRECATED_equipment_price',
        ),
    ]
