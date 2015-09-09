# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0008_auto_20150908_1529'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ('last_name', 'first_name')},
        ),
    ]
