# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tank', '0010_auto_20151101_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tank',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active', help_text='Designates whether this tank should be treated as active.             Unselect this instead of deleting tanks.'),
        ),
    ]
