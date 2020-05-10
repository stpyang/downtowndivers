'''Copyright 2016 DDNY New York. All Rights Reserved.'''

from django.forms import ModelForm, RadioSelect

from .models import Vip


class VipForm(ModelForm):
    '''https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/'''

    class Meta:
        model = Vip
        fields = Vip.header_fields + Vip.tank_fields + Vip.internal_fields + \
            Vip.external_fields + Vip.threads_fields + Vip.valve_fields + \
            Vip.cylindercondition_fields + Vip.inspector_fields
        widgets = {
            'external_evidence_of_heat_damage': RadioSelect,
            'external_repainting': RadioSelect,
            'external_odor': RadioSelect,
            'external_bow': RadioSelect,
            'external_evidence_of_bulges': RadioSelect,
            'external_hammer_tone_test': RadioSelect,
            'external_line_corrosion': RadioSelect,
            'external_comparison_to_psi_standards': RadioSelect,
            'internal_comparison_to_psi_standards': RadioSelect,
            'threads_eddy_current_test': RadioSelect,
            'threads_comparison_to_psi_standards': RadioSelect,
            'valve_service_needed': RadioSelect,
            'valve_burst_disc_replaced': RadioSelect,
            'valve_oring_replaced': RadioSelect,
            'valve_dip_tube_replaced': RadioSelect,
            'valve_threads_checked': RadioSelect,
            'cylindercondition_sticker_affixed': RadioSelect,
            'cylindercondition_disposition': RadioSelect,
            'cylindercondition': RadioSelect,
        }
