# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import registration.models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0010_member_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='address',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='city',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='phone_number',
            field=models.CharField(max_length=12, blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='psi_number',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='state',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='zip_code',
            field=models.CharField(max_length=10, validators=[registration.models.ZipCodeValidator], blank=True),
        ),
    ]
