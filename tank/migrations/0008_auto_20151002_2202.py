# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tank', '0007_auto_20150930_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vip',
            name='inspector_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='vip',
            name='state',
            field=models.CharField(blank=True, max_length=2),
        ),
    ]
