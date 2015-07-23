# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tank', '0003_auto_20150827_0116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hydro',
            options={'ordering': ('date',)},
        ),
        migrations.AlterModelOptions(
            name='vip',
            options={'ordering': ('date',)},
        ),
    ]
