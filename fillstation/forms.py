'''Copyright 2016 DDNY. All Rights Reserved.'''

from itertools import chain, groupby

from django import forms

from registration.models import Member
from tank.models import Tank
from gas.models import Gas


class MemberChoiceField(forms.ModelChoiceField):
    '''https://docs.djangoproject.com/en/2.2/ref/forms/fields/#django.forms.ModelChoiceField'''

    def __init__(self):
        super(MemberChoiceField, self).__init__(
            queryset=Member.objects.order_by("first_name"),
            empty_label="",
            to_field_name="username",
        )

    def label_from_instance(self, obj):
        return obj.first_name


class BlenderChoiceField(forms.ModelChoiceField):
    '''https://docs.djangoproject.com/en/2.2/ref/forms/fields/#django.forms.ModelChoiceField'''

    def __init__(self):
        super(BlenderChoiceField, self).__init__(
            queryset=Member.objects.is_blender().order_by("first_name"),
            empty_label="",
            to_field_name="username",
        )

    def label_from_instance(self, obj):
        return obj.first_name


class BlenderMixin(forms.Form):
    '''https://docs.djangoproject.com/en/2.2/topics/forms/#the-django-form-class'''

    blender = BlenderChoiceField()


class BillToMixin(forms.Form):
    '''https://docs.djangoproject.com/en/2.2/topics/forms/#the-django-form-class'''

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
    for (key, values) in groupby(tanks, lambda x: x[0]):
        codes = set()
        for value in values:
            codes.add((value[2], value[2]) if value[2] else (value[1], value[1]))
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
        queryset=Gas.objects.filter(is_banked=True),
        empty_label="",
        to_field_name="slug",
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

    breathable_gases = Gas.objects.exclude(name="Argon")
    gas_start_choices = [("", "")] + \
        [(g.slug, g.name) for g in breathable_gases] + \
        [("custom", "Custom")]
    gas_end_choices = [("", "")] + \
        [(g.slug, g.name) for g in breathable_gases] + \
        [("custom", "Custom")]
    gas_start = forms.ChoiceField(
        choices=gas_start_choices,
        required=True,
    )
    gas_end = forms.ChoiceField(
        choices=gas_end_choices,
        required=True,
    )

    # Gas inputs
    air = forms.BooleanField(required=False)
    oxygen = forms.BooleanField(required=False)
    helium = forms.BooleanField(required=False)
    nitrox_32 = forms.BooleanField(required=False)
    # nitrox_50 = forms.BooleanField(required=False)
    trimix_1845 = forms.BooleanField(required=False)
    trimix_2135 = forms.BooleanField(required=False)

    # Custom gases
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
    '''https://docs.djangoproject.com/en/2.2/topics/forms/#the-django-form-class'''
