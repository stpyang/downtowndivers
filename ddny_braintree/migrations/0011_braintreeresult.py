# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0010_auto_20150814_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='BraintreeResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('error', models.OneToOneField(to='ddny_braintree.BraintreeError', null=True, on_delete=models.CASCADE)),
                ('transaction', models.OneToOneField(to='ddny_braintree.BraintreeTransaction', null=True, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
