# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone
import tank.models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20150821_1830'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hydro',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(unique=True, max_length=30)),
                ('slug', models.SlugField()),
                ('metal', models.CharField(default='Al', max_length=8, choices=[('Al', 'Aluminum'), ('St', 'Steel')])),
                ('volume', models.FloatField()),
                ('pressure', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tank',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('serial_number', models.SlugField(unique=True)),
                ('code', models.SlugField(unique=True, help_text='Required. 50 characters or fewer.            Letters, numbers, underscores, and hyphens only.  Must be unique.')),
                ('doubles_code', models.SlugField(help_text='Optional. 50 characters or fewer.            Letters, numbers, underscores, and hyphens only.             Max two tanks per doubles code.', blank=True, default='')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active', help_text='Designates whether this user should be treated as active.             Unselect this instead of deleting tanks.')),
                ('owner', models.ForeignKey(to='registration.Member')),
                ('spec', models.ForeignKey(to='tank.Specification')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vip',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.DateField()),
                ('tank', models.ForeignKey(to='tank.Tank')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='hydro',
            name='tank',
            field=models.ForeignKey(to='tank.Tank'),
        ),
    ]
