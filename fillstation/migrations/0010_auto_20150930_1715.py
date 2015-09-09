# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0009_auto_20150915_1155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fill',
            old_name='tank_pressure',
            new_name='tank_working_pressure',
        ),
    ]
