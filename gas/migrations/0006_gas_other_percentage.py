# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('gas', '0005_auto_20150827_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='gas',
            name='other_percentage',
            field=models.DecimalField(max_digits=5, default=Decimal('0.00'), decimal_places=1, verbose_name='Percentage Other'),
        ),
    ]
