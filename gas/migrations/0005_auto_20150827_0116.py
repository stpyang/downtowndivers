# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gas', '0004_auto_20150820_1118'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gas',
            options={'ordering': ('name',), 'verbose_name_plural': 'Gases'},
        ),
    ]
