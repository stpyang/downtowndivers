# Generated by Django 2.2.1 on 2019-05-05 00:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0019_auto_20190503_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='fill',
            name='doubles_code',
            field=models.CharField(default=None, editable=False, max_length=30, null=True, verbose_name='Doubles code'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='cubic_feet',
            field=models.FloatField(editable=False, null=True, verbose_name='Cubic Feet'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='gas_name',
            field=models.CharField(default='', editable=False, max_length=30, null=True, verbose_name='Gas'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='gas_slug',
            field=models.SlugField(default='', editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='fill',
            name='psi_end',
            field=models.PositiveSmallIntegerField(editable=False, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4000)], verbose_name='Psi End'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='psi_start',
            field=models.PositiveSmallIntegerField(editable=False, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4000)], verbose_name='Psi Start'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='tank_code',
            field=models.SlugField(max_length=30, null=True, verbose_name='Tank Code'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='tank_factor',
            field=models.FloatField(editable=False, null=True, verbose_name='Tank Factor'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='tank_serial_number',
            field=models.CharField(editable=False, max_length=30, null=True, verbose_name='Tank Serial Number'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='tank_spec',
            field=models.CharField(editable=False, max_length=30, null=True, verbose_name='Tank Spec'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='tank_volume',
            field=models.FloatField(editable=False, null=True, verbose_name='Tank Volume'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='tank_working_pressure',
            field=models.PositiveSmallIntegerField(editable=False, null=True, verbose_name='Tank Pressure'),
        ),
    ]
