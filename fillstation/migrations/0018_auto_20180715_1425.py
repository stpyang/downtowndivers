# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0017_auto_20180715_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='fill',
            name='equipment_cost_fixed',
            field=models.DecimalField(verbose_name='Fixed Equipment Cost', decimal_places=2, max_digits=20, default=Decimal('0.00'), editable=False),
        ),
        migrations.AddField(
            model_name='fill',
            name='equipment_cost_proportional',
            field=models.DecimalField(verbose_name='Proportional Equipment Cost', decimal_places=2, max_digits=20, default=Decimal('0.00'), editable=False),
        ),
        migrations.AddField(
            model_name='fill',
            name='equipment_price_proportional',
            field=models.FloatField(verbose_name='Gas Price', default=0.0, editable=False),
        ),
        migrations.AddField(
            model_name='fill',
            name='is_equipment_surcharge',
            field=models.BooleanField(help_text='Designates whether this is an equipment surcharge', verbose_name='Is Blend', default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='fill',
            name='air_price',
            field=models.FloatField(verbose_name='Air Price', default=Decimal('0.00'), editable=False),
        ),
        migrations.AlterField(
            model_name='fill',
            name='argon_price',
            field=models.FloatField(verbose_name='Argon Price', default=Decimal('0.00'), editable=False),
        ),
        migrations.AlterField(
            model_name='fill',
            name='gas_name',
            field=models.CharField(verbose_name='Gas', max_length=30, default='', editable=False),
        ),
        migrations.AlterField(
            model_name='fill',
            name='gas_price',
            field=models.FloatField(verbose_name='Gas Price', default=0.0, editable=False),
        ),
        migrations.AlterField(
            model_name='fill',
            name='gas_slug',
            field=models.SlugField(editable=False, default=''),
        ),
        migrations.AlterField(
            model_name='fill',
            name='helium_price',
            field=models.FloatField(verbose_name='Helium Price', default=Decimal('0.00'), editable=False),
        ),
        migrations.AlterField(
            model_name='fill',
            name='oxygen_price',
            field=models.FloatField(verbose_name='Oxygen Price', default=Decimal('0.00'), editable=False),
        ),
    ]
