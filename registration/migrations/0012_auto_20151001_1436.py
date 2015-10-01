# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0011_auto_20150930_1715'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='psi_number',
            new_name='blender_certification_number',
        ),
        migrations.AddField(
            model_name='member',
            name='psi_inspector_number',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
