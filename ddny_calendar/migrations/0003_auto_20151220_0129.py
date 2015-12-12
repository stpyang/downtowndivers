# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_calendar', '0002_auto_20151212_1158'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('start_date',)},
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=80),
        ),
    ]
