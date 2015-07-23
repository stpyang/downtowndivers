# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('name', models.CharField(unique=True, max_length=30)),
                ('argon_percentage', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Percentage Argon')),
                ('helium_percentage', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Percentage Helium')),
                ('oxygen_percentage', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Percentage Oxygen')),
                ('is_banked', models.BooleanField(default=False, verbose_name='Is Banked', help_text='Designates whether this gas is banked.')),
            ],
            options={
                'verbose_name_plural': 'Gases',
            },
        ),
    ]
