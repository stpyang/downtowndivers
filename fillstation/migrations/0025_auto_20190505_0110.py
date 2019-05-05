# Generated by Django 2.2.1 on 2019-05-05 05:10

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0024_auto_20190505_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill',
            name='equipment_cost_proportional',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.08'), editable=False, max_digits=20, verbose_name='Proportional Equipment Cost'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='equipment_price_proportional',
            field=models.FloatField(default=0.0, editable=False, verbose_name='Equipment Price (per cubic foot)'),
        ),
    ]