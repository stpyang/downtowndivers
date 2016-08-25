# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0017_member_is_treasurer'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='honorary_member',
            field=models.BooleanField(help_text='Honorary members can view the website and have their tanks filled at the club', default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_treasurer',
            field=models.BooleanField(help_text='Designates whether the member can see additional fillstation accounting info', default=False),
        ),
    ]
