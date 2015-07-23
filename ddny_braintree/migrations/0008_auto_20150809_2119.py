# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0007_braintreeerror'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='braintreeerror',
            options={'verbose_name': 'Error'},
        ),
        migrations.AlterModelOptions(
            name='braintreetransaction',
            options={'verbose_name': 'Transaction'},
        ),
    ]
