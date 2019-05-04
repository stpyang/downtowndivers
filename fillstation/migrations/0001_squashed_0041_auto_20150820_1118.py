# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import model_utils.fields
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('fillstation', '0001_initial'), ('fillstation', '0002_auto_20150723_2025'), ('fillstation', '0003_auto_20150724_1251'), ('fillstation', '0004_auto_20150726_1401'), ('fillstation', '0005_auto_20150726_1406'), ('fillstation', '0006_auto_20150726_1413'), ('fillstation', '0007_auto_20150726_1417'), ('fillstation', '0008_auto_20150726_1629'), ('fillstation', '0009_auto_20150726_1931'), ('fillstation', '0010_auto_20150726_2216'), ('fillstation', '0011_auto_20150727_0354'), ('fillstation', '0012_auto_20150727_0459'), ('fillstation', '0013_auto_20150727_1428'), ('fillstation', '0014_fill_gas_price'), ('fillstation', '0015_auto_20150728_0818'), ('fillstation', '0016_gas_is_banked'), ('fillstation', '0017_remove_gas_is_banked'), ('fillstation', '0018_auto_20150731_0126'), ('fillstation', '0019_fill_is_blend'), ('fillstation', '0020_auto_20150801_2251'), ('fillstation', '0021_auto_20150801_2305'), ('fillstation', '0022_auto_20150801_2317'), ('fillstation', '0023_auto_20150802_2111'), ('fillstation', '0024_auto_20150802_2233'), ('fillstation', '0025_auto_20150803_1820'), ('fillstation', '0026_auto_20150803_1828'), ('fillstation', '0027_auto_20150803_1855'), ('fillstation', '0028_auto_20150803_2137'), ('fillstation', '0029_auto_20150806_2106'), ('fillstation', '0030_remove_fill_braintree_transaction_status'), ('fillstation', '0031_fill_braintree_transaction'), ('fillstation', '0032_fill_is_paid'), ('fillstation', '0033_auto_20150807_1307'), ('fillstation', '0034_auto_20150807_1411'), ('fillstation', '0035_auto_20150811_1926'), ('fillstation', '0036_auto_20150814_2159'), ('fillstation', '0037_auto_20150814_2242'), ('fillstation', '0038_delete_gas'), ('fillstation', '0039_auto_20150819_2043'), ('fillstation', '0040_auto_20150819_2127'), ('fillstation', '0041_auto_20150820_1118')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tank', '0001_initial'),
        ('ddny_braintree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Time')),
                ('psi_start', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Psi Start')),
                ('psi_end', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Psi End')),
                ('tank_volume', models.FloatField(default=0, editable=False, verbose_name='Tank Volume')),
                ('tank_pressure', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Tank Pressure')),
                ('tank_factor', models.FloatField(default=0, editable=False, verbose_name='Tank Factor')),
                ('equipment_cost', models.DecimalField(decimal_places=2, max_digits=20, default=Decimal('0.070000000000000006661338147750939242541790008544921875'), editable=False, verbose_name='Equipment Cost')),
                ('cubic_feet', models.FloatField(default=0.0, editable=False, verbose_name='Cubic Feet')),
                ('equipment_price', models.DecimalField(decimal_places=2, max_digits=20, default=Decimal('0'), editable=False, verbose_name='Equipment Price')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=20, default=Decimal('0'), editable=False, verbose_name='Total Price')),
                ('bill_to', models.ForeignKey(related_name='fillstation_fill_bill_to_related', verbose_name='Bill To', to='registration.Member', on_delete=models.CASCADE)),
                ('blender', models.ForeignKey(related_name='fillstation_fill_blender_related', verbose_name='Blender', to='registration.Member', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(related_name='fillstation_fill_owner_related', verbose_name='User', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('air_price', models.FloatField(editable=False, verbose_name='Air Price')),
                ('argon_price', models.FloatField(editable=False, verbose_name='Argon Price')),
                ('helium_price', models.FloatField(editable=False, verbose_name='Helium Price')),
                ('oxygen_price', models.FloatField(editable=False, verbose_name='Oxygen Price')),
                ('air_cost', models.DecimalField(decimal_places=2, max_digits=20, default=Decimal('0.0200000000000000004163336342344337026588618755340576171875'), editable=False, verbose_name='Air Cost')),
                ('argon_cost', models.DecimalField(decimal_places=2, max_digits=20, default=Decimal('1'), editable=False, verbose_name='Argon Cost')),
                ('helium_cost', models.DecimalField(decimal_places=2, max_digits=20, default=Decimal('1.3000000000000000444089209850062616169452667236328125'), editable=False, verbose_name='Helium Cost')),
                ('oxygen_cost', models.DecimalField(decimal_places=2, max_digits=20, default=Decimal('0.200000000000000011102230246251565404236316680908203125'), editable=False, verbose_name='Oxygen Cost')),
                ('gas_name', models.CharField(verbose_name='Gas', editable=False, max_length=30)),
                ('tank_code', models.SlugField(verbose_name='Tank Code', max_length=30, editable=False)),
                ('tank_serial_number', models.CharField(verbose_name='Tank Serial Number', editable=False, max_length=30)),
                ('tank_spec', models.CharField(verbose_name='Tank Spec', editable=False, max_length=30)),
                ('gas_price', models.DecimalField(decimal_places=2, max_digits=20, default=Decimal('0'), editable=False, verbose_name='Gas Price')),
                ('is_blend', models.BooleanField(verbose_name='Is Blend', default=False, editable=False, help_text='Designates whether this fill was part of a partial pressure blend')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Is Paid')),
                ('braintree_transaction_id', models.CharField(verbose_name='Braintree', default='', editable=False, max_length=6)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('gas_slug', models.SlugField(editable=False)),
            ],
        ),
    ]
