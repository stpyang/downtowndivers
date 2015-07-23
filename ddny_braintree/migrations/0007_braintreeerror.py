# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0006_auto_20150807_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='BraintreeError',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('message', models.CharField(editable=False, max_length=255)),
                ('params', models.CharField(editable=False, max_length=255)),
            ],
        ),
    ]
