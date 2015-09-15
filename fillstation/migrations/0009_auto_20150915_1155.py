# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0008_auto_20150914_0231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fill',
            options={'ordering': ('-datetime', '-id')},
        ),
    ]
