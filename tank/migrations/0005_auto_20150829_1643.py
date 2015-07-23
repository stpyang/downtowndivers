# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tank', '0004_auto_20150827_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specification',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
