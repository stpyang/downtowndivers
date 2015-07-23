# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20150821_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='autopay_fills',
            field=models.BooleanField(help_text='Raph only!', default=False),
        ),
    ]
