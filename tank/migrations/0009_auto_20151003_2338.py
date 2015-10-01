# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tank', '0008_auto_20151002_2202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hydro',
            options={'ordering': ('-date',)},
        ),
        migrations.RenameField(
            model_name='vip',
            old_name='tank_current_hydro_date',
            new_name='tank_last_hydro_date',
        ),
    ]
