# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0009_auto_20150814_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='braintreetransaction',
            name='status_changed',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status'),
        ),
        migrations.AlterField(
            model_name='braintreetransaction',
            name='status',
            field=model_utils.fields.StatusField(db_index=True, default='', choices=[(0, 'dummy')], no_check_for_status=True, max_length=100, verbose_name='Status'),
        ),
    ]
