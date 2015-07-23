# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0004_auto_20150826_0359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fill',
            options={'ordering': ('-id',)},
        ),
    ]
