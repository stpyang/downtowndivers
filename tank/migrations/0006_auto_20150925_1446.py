# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tank', '0005_auto_20150829_1643'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vip',
            options={'ordering': ('-date',)},
        ),
        migrations.RenameField(
            model_name='specification',
            old_name='pressure',
            new_name='working_pressure',
        ),
        migrations.RemoveField(
            model_name='specification',
            name='metal',
        ),
        migrations.AddField(
            model_name='specification',
            name='material',
            field=models.CharField(max_length=8, choices=[('Aluminum', 'Aluminum'), ('Steel', 'Steel'), ('FRP', 'FRP'), ('Composite', 'Composite')], default='Aluminum'),
        ),
        migrations.AddField(
            model_name='vip',
            name='address',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='city',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='cylindercondition',
            field=models.CharField(max_length=8, choices=[('Accept', 'Accept'), ('Reject', 'Reject'), ('Condemn', 'Condemn')], default='Accept'),
        ),
        migrations.AddField(
            model_name='vip',
            name='cylindercondition_clean',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vip',
            name='cylindercondition_discard',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vip',
            name='cylindercondition_hydro',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vip',
            name='cylindercondition_inspector_initials',
            field=models.CharField(max_length=5, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='cylindercondition_other',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vip',
            name='cylindercondition_sticker_affixed',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes'),
        ),
        migrations.AddField(
            model_name='vip',
            name='cylindercondition_sticker_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='cylindercondition_sticker_notation',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='cylindercondition_tumble',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vip',
            name='external_bow',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='external_comparison_to_psi_standards',
            field=models.CharField(max_length=8, choices=[('Accept', 'Accept'), ('Reject', 'Reject'), ('Condemn', 'Condemn')], default='Accept'),
        ),
        migrations.AddField(
            model_name='vip',
            name='external_description_of_surface',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='external_evidence_of_bulges',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='external_evidence_of_heat_damage',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='external_hammer_tone_test',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='external_line_corrosion',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='external_odor',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='external_repainting',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='inspectors_name',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='inspectors_psi_number',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='internal_comparison_to_psi_standards',
            field=models.CharField(max_length=8, choices=[('Accept', 'Accept'), ('Reject', 'Reject'), ('Condemn', 'Condemn')], default='Accept'),
        ),
        migrations.AddField(
            model_name='vip',
            name='internal_composition_of_contents',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='internal_description_of_surface',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='internal_pitting',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='phone_number',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='state',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='tank_current_hydro_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='tank_first_hydro_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='tank_material',
            field=models.CharField(max_length=8, choices=[('Aluminum', 'Aluminum'), ('Steel', 'Steel'), ('FRP', 'FRP'), ('Composite', 'Composite')], default='Aluminum'),
        ),
        migrations.AddField(
            model_name='vip',
            name='tank_owners_name',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='tank_serial_number',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='tank_spec_name',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='tank_specification',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='tank_working_pressure',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='threads_comparison_to_psi_standards',
            field=models.CharField(max_length=8, choices=[('Accept', 'Accept'), ('Reject', 'Reject'), ('Condemn', 'Condemn')], default='Accept'),
        ),
        migrations.AddField(
            model_name='vip',
            name='threads_crack_assessment',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='threads_description',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='threads_eddy_current_test',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='threads_oring_gland_surface',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='valve_burst_disc_replaced',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='valve_dip_tube_replaced',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='valve_oring_replaced',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='valve_service_needed',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='valve_thread_condition',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='vip',
            name='valve_threads_checked',
            field=models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'),
        ),
        migrations.AddField(
            model_name='vip',
            name='zip_code',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
