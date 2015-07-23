# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tank', '0002_auto_20150825_0000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hydro',
            options={'ordering': ('-date',)},
        ),
        migrations.AlterModelOptions(
            name='specification',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='tank',
            options={'ordering': ('owner__username', 'code')},
        ),
        migrations.AlterModelOptions(
            name='vip',
            options={'ordering': ('-date',)},
        ),
    ]
