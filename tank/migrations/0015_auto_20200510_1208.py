# Generated by Django 2.2.10 on 2020-05-10 16:08

from django.db import migrations, models
import registration.models


class Migration(migrations.Migration):

    dependencies = [
        ('tank', '0014_auto_20200510_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vip',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AlterField(
            model_name='vip',
            name='zip_code',
            field=models.CharField(blank=True, default='', max_length=10, validators=[registration.models.ZipCodeValidator]),
            preserve_default=False,
        ),
    ]