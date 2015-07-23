# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gas', '0003_gas_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gas',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
