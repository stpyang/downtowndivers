# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_calendar', '0005_auto_20151220_0241'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('start_date', 'end_date')},
        ),
    ]
