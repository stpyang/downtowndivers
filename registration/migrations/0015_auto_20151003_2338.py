# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0014_auto_20151002_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyDues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('braintree_transaction_id', models.CharField(max_length=30, verbose_name='Braintree', editable=False, default='')),
                ('is_paid', models.BooleanField(verbose_name='Is Paid', default=False)),
                ('months', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Monthly Dues',
            },
        ),
        migrations.AlterField(
            model_name='member',
            name='member_since',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='monthlydues',
            name='member',
            field=models.ForeignKey(to='registration.Member'),
        ),
    ]
