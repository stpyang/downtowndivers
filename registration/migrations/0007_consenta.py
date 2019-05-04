# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
# import jsignature.fields
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20150827_0116'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsentA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('member_name', models.CharField(max_length=30)),
                # ('member_signature', jsignature.fields.JSignatureField()),
                ('member_signature_date', models.DateField()),
                ('witness_name', models.CharField(max_length=30)),
                # ('witness_signature', jsignature.fields.JSignatureField()),
                ('witness_signature_date', models.DateField()),
                ('consent_is_experienced_certified_diver', models.BooleanField()),
                ('consent_club_is_non_profit', models.BooleanField()),
                ('consent_vip_tank', models.BooleanField()),
                ('consent_examine_tank', models.BooleanField()),
                ('consent_no_unsafe_tank', models.BooleanField()),
                ('consent_analyze_gas', models.BooleanField()),
                ('consent_compressed_gas_risk', models.BooleanField()),
                ('consent_diving_risk', models.BooleanField()),
                ('consent_sole_responsibility', models.BooleanField()),
                ('consent_do_not_sue', models.BooleanField()),
                ('consent_strenuous_activity_risk', models.BooleanField()),
                ('consent_inspect_equipment', models.BooleanField()),
                ('consent_lawful_age', models.BooleanField()),
                ('consent_release_of_risk', models.BooleanField()),
                ('member', models.ForeignKey(to='registration.Member', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Consent v1.0',
                'verbose_name_plural': 'Consents v1.0',
            },
        ),
    ]
