# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_auto_20151001_1436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='blender_certification_number',
            new_name='blender_certification',
        ),
    ]
