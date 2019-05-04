# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_consenta'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consenta',
            options={'verbose_name_plural': 'Consents v1.0', 'verbose_name': 'Consent v1.0'},
        ),
    ]
