# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0002_auto_20150825_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill',
            name='equipment_price',
            field=models.FloatField(editable=False, verbose_name='Equipment Price'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='gas_price',
            field=models.FloatField(editable=False, verbose_name='Gas Price'),
        ),
    ]
