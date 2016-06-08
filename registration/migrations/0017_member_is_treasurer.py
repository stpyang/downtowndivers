# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0016_auto_20160603_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_treasurer',
            field=models.BooleanField(help_text='Designates whether the member can see other member prepay info', default=False),
        ),
    ]
