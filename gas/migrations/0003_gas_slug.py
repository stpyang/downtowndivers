# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gas', '0002_auto_20150818_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='gas',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
