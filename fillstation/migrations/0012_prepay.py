# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0016_auto_20160603_1037'),
        ('fillstation', '0011_auto_20151021_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prepay',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('braintree_transaction_id', models.CharField(default='', editable=False, max_length=30, verbose_name='Braintree')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Is Paid')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Amount')),
                ('fill', models.ForeignKey(blank=True, default=None, null=True, to='fillstation.Fill')),
                ('member', models.ForeignKey(to='registration.Member')),
            ],
            options={
                'verbose_name_plural': 'Prepay',
            },
        ),
    ]
