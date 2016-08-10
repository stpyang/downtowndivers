'''Copyright 2016 DDNY. All Rights Reserved.'''

from collections import defaultdict
from itertools import chain, groupby

from django import forms

from registration.models import Member
from tank.models import Tank
from gas.models import Gas


class MemberChoiceField(forms.ModelChoiceField):
    def __init__(self):
        super(MemberChoiceField, self).__init__(
            queryset=Member.objects.order_by("first_name"),
            empty_label="",
            to_field_name="username",
        )

    def label_from_instance(self, obj):
        return obj.first_name


class BlenderChoiceField(forms.ModelChoiceField):
    def __init__(self):
        super(BlenderChoiceField, self).__init__(
            queryset=Member.objects.is_blender().order_by("first_name"),
            empty_label="",
            to_field_name="username",
        )

    def label_from_instance(self, obj):
        return obj.first_name


class BlenderMixin(forms.Form):
    blender = BlenderChoiceField()


class BillToMixin(forms.Form):
    bill_to = MemberChoiceField()


def get_tank_field(user):
    '''Return the list of tanks grouped by owner'''
    tanks = []
    if hasattr(user, "member"):
        user_tanks = Tank.objects.active().filter(owner=user.member)
        non_user_tanks = Tank.objects.active().exclude(owner=user.member)
        tanks = [(t.owner.first_name, t.code, t.doubles_code) for t in (
            chain(user_tanks, non_user_tanks)
        )]
    else:
        tanks = [(t.owner.first_name, t.code, t.doubles_code) for t in (
            Tank.objects.active()
        )]
    choices = []
    for (key, value) in groupby(tanks, lambda x: x[0]):
        codes = set()
        for v in value:
            codes.add((v[2], v[2]) if v[2] else (v[1], v[1]))
        choices += [(key, sorted(list(codes)))]
    return forms.ChoiceField(
        choices=choices,
        required=True,
    )


class FillForm(BlenderMixin, BillToMixin, forms.Form):
    '''
    This is the form object for the fill station fill web site.
    It is only used to generate fields.
    Submission is handled by jQuery scripts.
    Only people with permissions "can add fill" can be a blender.
    Only people marked as staff (i.e. club members) can pay for gas fills
    '''

    def __init__(self, user, *args, **kwargs):
        super(FillForm, self).__init__(*args, **kwargs)
        self.fields["tank"] = get_tank_field(user)

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


class BlendForm(BlenderMixin, BillToMixin, forms.Form):
    '''
    This is the form object for the fill station blend web site.
    It is only used to generate fields.
    Submission is handled by jQuery scripts.
    Only people with permissions "can add fill" can be a blender.
    Only people marked as staff (i.e. club members) can pay for gas fills
    '''

    def __init__(self, user, *args, **kwargs):
        super(BlendForm, self).__init__(*args, **kwargs)
        self.fields["tank"] = get_tank_field(user)

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
    trimix_10_70 = forms.BooleanField()
    trimix_18_45 = forms.BooleanField()
    trimix_21_35 = forms.BooleanField()

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
