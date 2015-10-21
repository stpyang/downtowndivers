# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0010_auto_20150930_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill',
            name='tank_code',
            field=models.SlugField(verbose_name='Tank Code', max_length=30),
        ),
    ]
