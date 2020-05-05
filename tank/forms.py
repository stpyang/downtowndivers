'''Copyright 2016 DDNY New York. All Rights Reserved.'''

from django import forms

from .models import Vip


class VipForm(forms.ModelForm):
    class Meta:
        model = Vip
        fields = Vip.header_fields + Vip.tank_fields + Vip.internal_fields + \
            Vip.external_fields + Vip.threads_fields + Vip.valve_fields + \
            Vip.cylindercondition_fields + Vip.inspector_fields
        widgets = {
            "external_evidence_of_heat_damage": forms.RadioSelect,
            "external_repainting": forms.RadioSelect,
            "external_odor": forms.RadioSelect,
            "external_bow": forms.RadioSelect,
            "external_evidence_of_bulges": forms.RadioSelect,
            "external_hammer_tone_test": forms.RadioSelect,
            "external_line_corrosion": forms.RadioSelect,
            "external_comparison_to_psi_standards": forms.RadioSelect,
            "internal_comparison_to_psi_standards": forms.RadioSelect,
            "threads_eddy_current_test": forms.RadioSelect,
            "threads_comparison_to_psi_standards": forms.RadioSelect,
            "valve_service_needed": forms.RadioSelect,
            "valve_burst_disc_replaced": forms.RadioSelect,
            "valve_oring_replaced": forms.RadioSelect,
            "valve_dip_tube_replaced": forms.RadioSelect,
            "valve_threads_checked": forms.RadioSelect,
            "cylindercondition_sticker_affixed": forms.RadioSelect,
            "cylindercondition_disposition": forms.RadioSelect,
            "cylindercondition": forms.RadioSelect,
        }
