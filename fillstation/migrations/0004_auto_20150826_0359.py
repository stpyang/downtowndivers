# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0003_auto_20150825_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill',
            name='psi_end',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4000)], editable=False, verbose_name='Psi End', default=0),
        ),
        migrations.AlterField(
            model_name='fill',
            name='psi_start',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4000)], editable=False, verbose_name='Psi Start', default=0),
        ),
    ]
