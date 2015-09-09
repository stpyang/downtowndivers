# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tank', '0006_auto_20150925_1446'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vip',
            old_name='inspectors_name',
            new_name='inspector_name',
        ),
        migrations.RenameField(
            model_name='vip',
            old_name='inspectors_psi_number',
            new_name='inspector_psi_number',
        ),
    ]
