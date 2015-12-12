# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_calendar', '0004_auto_20151220_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='show_on_homepage',
            field=models.NullBooleanField(default=False),
        ),
    ]
