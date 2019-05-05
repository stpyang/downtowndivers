# Generated by Django 2.2.1 on 2019-05-05 14:55

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0025_auto_20190505_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill',
            name='doubles_code',
            field=models.CharField(default=None, max_length=30, null=True, verbose_name='Doubles code'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='is_equipment_surcharge',
            field=models.BooleanField(default=False, help_text='Designates whether this is an equipment surcharge', verbose_name='Is Equipment Surcharge'),
        ),
        migrations.AlterField(
            model_name='fill',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20, verbose_name='Total Price (for gas or equipment)'),
        ),
    ]
