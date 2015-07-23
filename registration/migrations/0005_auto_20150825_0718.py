# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import registration.models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20150824_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, validators=[registration.models.validate_user]),
        ),
    ]
