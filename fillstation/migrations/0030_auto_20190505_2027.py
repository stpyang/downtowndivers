# Generated by Django 2.2.1 on 2019-05-06 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fillstation', '0029_auto_20190505_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill',
            name='equipment_surcharge_key',
            field=models.CharField(blank=True, default=None, max_length=30, null=True, verbose_name='Equipment Surcharge Key'),
        ),
    ]