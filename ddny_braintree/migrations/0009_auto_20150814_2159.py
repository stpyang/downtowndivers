# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ddny_braintree', '0008_auto_20150809_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='braintreeerror',
            name='created',
            field=model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='braintreeerror',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='braintreepaypaldetails',
            name='created',
            field=model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='braintreepaypaldetails',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='braintreetransaction',
            name='created',
            field=model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='braintreetransaction',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False),
        ),
    ]
