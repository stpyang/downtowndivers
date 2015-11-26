# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tank', '0009_auto_20151003_2338'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tank',
            options={'ordering': ('owner__first_name', 'code')},
        ),
    ]
