# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0015_auto_20151003_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlydues',
            name='months',
            field=models.PositiveIntegerField(),
        ),
    ]
