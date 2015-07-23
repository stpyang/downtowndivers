# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20150822_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='is_blender',
            field=models.BooleanField(default=False, help_text='Designates whether the member is a certified gas blender'),
        ),
        migrations.AlterField(
            model_name='member',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
