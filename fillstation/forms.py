'''Copyright 2015 DDNY. All Rights Reserved.'''

from collections import defaultdict

from django import forms

from registration.models import Member
from tank.models import Tank
from gas.models import Gas


class MemberChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.first_name


class BlenderMixin(forms.Form):
    blender = MemberChoiceField(
        queryset=Member.objects.is_blender().order_by("first_name"),
        empty_label="",
        to_field_name="username",
    )


class BillToMixin(forms.Form):
    bill_to = MemberChoiceField(
        queryset=Member.objects.order_by("first_name"),
        empty_label="",
        to_field_name="username",
    )


# TODO(stpyang): refactor
class TanksMixin(forms.Form):
    '''Return the list of tanks grouped by owner'''
    __tanks = [(t.owner.first_name, t.code, t.doubles_code) for t in (
        Tank.objects.active()
    )]
    __grouped_tanks = defaultdict(set)
    for t in __tanks:
        __grouped_tanks[t[0]].add(t[2] if t[2] else t[1])
    __choices = []
    for g in __grouped_tanks:
        __codes = [(x, x) for x in sorted(__grouped_tanks[g])]
        __choices += [(g, __codes)]
    tank = forms.ChoiceField(
        choices=__choices,
        required=True,
    )


class FillForm(BlenderMixin, BillToMixin, TanksMixin, forms.Form):
    '''
    This is the form object for the fill station fill web site.
    It is only used to generate fields.
    Submission is handled by jQuery scripts.
    Only people with permissions "can add fill" can be a blender.
    Only people marked as staff (i.e. club members) can pay for gas fills
    '''
    gas = forms.ModelChoiceField(
        queryset=Gas.objects.is_banked(),
        empty_label="",
        to_field_name="name",
    )
    psi_start = forms.IntegerField(
        min_value=0,
        max_value=4000,
        required=True,
    )
    psi_end = forms.IntegerField(
        min_value=0,
        max_value=4000,
        required=True,
    )


class BlendForm(BlenderMixin, BillToMixin, TanksMixin, forms.Form):
    '''
    This is the form object for the fill station blend web site.
    It is only used to generate fields.
    Submission is handled by jQuery scripts.
    Only people with permissions "can add fill" can be a blender.
    Only people marked as staff (i.e. club members) can pay for gas fills
    '''

    gases = [("", "")] + \
        [(g.name, g.name) for g in Gas.objects.exclude(name="Argon")] + \
        [("Custom", "Custom")]
    gas_start = forms.ChoiceField(
        choices=gases,
        required=True,
    )
    gas_end = forms.ChoiceField(
        choices=gases,
        required=True,
    )

    air = forms.BooleanField()
    oxygen = forms.BooleanField()
    helium = forms.BooleanField()
    nitrox_32 = forms.BooleanField()
    nitrox_50 = forms.BooleanField()
    trimix_18_45 = forms.BooleanField()

    helium_start = forms.IntegerField(
        min_value=0,
        max_value=100,
        required=True,
    )
    oxygen_start = forms.IntegerField(
        min_value=0,
        max_value=100,
        required=True,
    )
    psi_start = forms.IntegerField(
        min_value=0,
        max_value=4000,
        required=True,
    )
    helium_end = forms.IntegerField(
        min_value=0,
        max_value=100,
        required=True,
    )
    oxygen_end = forms.IntegerField(
        min_value=0,
        max_value=100,
        required=True,
    )
    psi_end = forms.IntegerField(
        min_value=0,
        max_value=4000,
        required=True,
    )


class BillToForm(BillToMixin, forms.Form):
    pass
