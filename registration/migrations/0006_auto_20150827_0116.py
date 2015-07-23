# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_auto_20150825_0718'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ('username',)},
        ),
    ]
