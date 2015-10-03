# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0013_auto_20151001_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='member_since',
            field=models.DateField(default=datetime.date(2015, 10, 2)),
        ),
        migrations.AlterField(
            model_name='member',
            name='state',
            field=models.CharField(blank=True, max_length=2),
        ),
    ]
