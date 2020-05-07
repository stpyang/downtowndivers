'''Copyright 2016 DDNY New York. All Rights Reserved.'''

import csv
import json

from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView

from ddny.decorators import consent_required, warn_if_superuser
from ddny.mixins import ConsentRequiredMixin, WarnIfSuperuserMixin
from ddny.views import AbstractActionMixin
from fillstation.models import Fill
from registration.models import Member
from .forms import VipForm
from .models import Hydro, Specification, Tank, Vip


class HydroInline(InlineFormSetFactory):
    model = Hydro
    fields = ['date']


class SpecActionMixin(AbstractActionMixin):
    '''set a message of a specification is created or saved'''

    @property
    def success_msg(self):
        return super(SpecActionMixin).success_msg

    @property
    def cancel_msg(self):
        return super(SpecActionMixin).cancel_msg

    @property
    def cancel_url(self):
        return super(SpecActionMixin).cancel_url

    fields = (
        "name",
        "material",
        "volume",
        "working_pressure",
    )


class SpecCreate(
    LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, SpecActionMixin, CreateView
):
    '''create a new Specification'''
    model = Specification
    template_name = "tank/spec_form.html"

    @property
    def success_msg(self):
        form = self.get_form()
        name = form['name'].value()
        return "The specification \"{0}\" was created successfully!".format(name)

    @property
    def cancel_msg(self):
        return "The specification was not created!"

    @property
    def cancel_url(self):
        return reverse("spec_list")


class SpecDetail(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, DetailView):
    context_object_name = "spec"
    model = Specification
    slug_field = "slug"
    template_name = "tank/spec_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SpecDetail, self).get_context_data(**kwargs)
        context["tank_list"] = Tank.objects.filter(spec=self.object)
        return context


class SpecList(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, ListView):
    model = Specification
    context_object_name = "spec_list"
    template_name = "tank/spec_list.html"


class SpecUpdate(
    LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, SpecActionMixin, UpdateView
):
    '''update Specification info'''
    context_object_name = "spec"
    model = Specification
    slug_field = "slug"
    template_name = "tank/spec_form.html"

    @property
    def success_msg(self):
        return "The specification \"{0}\" was updated successfully!".format(self.get_object())

    @property
    def cancel_msg(self):
        return "The specification \"{0}\" was not updated!".format(self.get_object())

    @property
    def cancel_url(self):
        return self.get_object().get_absolute_url()


class TankActionMixin(AbstractActionMixin):
    '''set a message of a specification is created or saved'''

    @property
    def success_msg(self):
        return super(TankActionMixin).success_msg

    @property
    def cancel_msg(self):
        return super(TankActionMixin).cancel_msg

    @property
    def cancel_url(self):
        return super(TankActionMixin).cancel_url

    fields = (
        "serial_number",
        "owner",
        "code",
        "doubles_code",
        "spec",
        "is_active",
    )


class TankCreate(
    LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, TankActionMixin,
    CreateWithInlinesView
):
    '''create a new Tank'''
    model = Tank

    @property
    def success_msg(self):
        form = self.get_form()
        code = form['code'].value()
        return "The tank \"{0}\" was created successfully.".format(code)

    @property
    def cancel_msg(self):
        return "The tank was not created!"

    @property
    def cancel_url(self):
        return reverse("tank:list")


class TankDetail(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, DetailView):
    context_object_name = "tank"
    model = Tank
    slug_field = "code"

    def get_context_data(self, **kwargs):
        context = super(TankDetail, self).get_context_data(**kwargs)
        context["hydros"] = Hydro.objects.filter(tank=self.object)
        context["vip_list"] = Vip.objects.filter(tank=self.object)
        context["fill_list"] = Fill.objects.filter(
            tank_serial_number=self.object.serial_number
        )[:10]
        return context


class TankList(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, ListView):
    model = Tank
    context_object_name = "tank_list"
    default_sort_params = ["owner__first_name", "code"]

    def get_queryset(self):
        return Tank.objects.filter(is_active=True)


class TankUpdate(
    LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, TankActionMixin,
    UpdateWithInlinesView
):
    '''update Tank info'''
    context_object_name = "tank"
    model = Tank
    slug_field = "code"
    inlines = [HydroInline]

    @property
    def success_msg(self):
        return "The tank \"{0}\" was updated successfully.".format(self.get_object())

    @property
    def cancel_msg(self):
        return "The tank \"{0}\" was not updated!".format(self.get_object())

    @property
    def cancel_url(self):
        return self.get_object().get_absolute_url()


class VipCreate(
    LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, AbstractActionMixin, CreateView
):
    '''create a new Vip'''
    form_class = VipForm
    model = Vip

    @property
    def success_msg(self):
        return "The VIP form was created successfully!"

    @property
    def cancel_msg(self):
        return "The VIP form was not created!"

    @property
    def cancel_url(self):
        return reverse("vip_list")

    def get_context_data(self, **kwargs):
        inspector_info = {}
        for inspector in Member.objects.exclude(psi_inspector_number=""):
            inspector_info[inspector.full_name] = inspector.psi_inspector_number
        context = super(VipCreate, self).get_context_data(**kwargs)
        context["tank"] = Tank.objects.get(code=self.kwargs.get("slug"))
        context["inspector_info"] = json.dumps(inspector_info)
        return context


class VipDetail(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, DetailView):
    context_object_name = "vip"
    model = Vip
    slug_field = "id"


class VipList(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, ListView):
    model = Vip
    context_object_name = "vip_list"

    def get_queryset(self):
        return Vip.objects.current()


class VipUpdate(
    LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, AbstractActionMixin, UpdateView
):
    '''update Vip info'''
    context_object_name = "vip"
    form_class = VipForm
    model = Vip

    @property
    def success_msg(self):
        return "The VIP form was updated successfully!"

    @property
    def cancel_msg(self):
        return "The VIP form was not updated!"

    @property
    def cancel_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        inspector_info = {}
        for inspector in Member.objects.exclude(psi_inspector_number=""):
            inspector_info[inspector.full_name] = inspector.psi_inspector_number
        context = super(VipUpdate, self).get_context_data(**kwargs)
        vip = Vip.objects.get(id=self.kwargs.get("pk"))
        context["tank"] = Tank.objects.get(id=vip.tank.id)
        context["inspector_info"] = json.dumps(inspector_info)
        return context


@warn_if_superuser
@consent_required
@login_required
def eighteen_step(request):
    ''' A page for filling tanks from the banked gases'''
    return render(request, "tank/eighteen_step.html")


@consent_required
@login_required
def download(request):  # pylint: disable=unused-argument
    "Download all the tanks into a csv file"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=ddny_tanks"

    writer = csv.writer(response)
    fields = Tank._meta.fields  # pylint: disable=W0212
    writer.writerow([field.name for field in fields])
    for tank in Tank.objects.all():
        writer.writerow([str(getattr(tank, field.name)) for field in fields])

    return response
