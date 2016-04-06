
'''Copyright 2016 DDNY New York. All Rights Reserved.'''

from braces.views import LoginRequiredMixin
from extra_views import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ddny.decorators import consent_required, warn_if_superuser
from ddny.mixins import (
    ConsentRequiredMixin, WarnIfSuperuserMixin, SortableMixin
)
from django.shortcuts import render
from ddny.views import AbstractActionMixin
from fillstation.models import Fill
from .forms import VipForm
from .models import Hydro, Specification, Tank, Vip


class HydroInline(InlineFormSet):
    model = Hydro
    extra = 1


class SpecActionMixin(AbstractActionMixin):
    '''set a message of a specification is created or saved'''
    fields = (
        "name",
        "material",
        "volume",
        "working_pressure",
    )


class SpecCreate(LoginRequiredMixin,
                 ConsentRequiredMixin,
                 WarnIfSuperuserMixin,
                 SpecActionMixin,
                 CreateView):
    '''create a new Specification'''
    model = Specification
    template_name = "tank/spec_form.html"

    def success_msg(self):
        form = self.get_form()
        name = form['name'].value()
        return "The specification \"{0}\" was created successfully!".format(name)

    def cancel_msg(self):
        return "The specification was not created!"

    def cancel_url(self):
        return reverse("spec_list")


class SpecDetail(LoginRequiredMixin,
                 ConsentRequiredMixin,
                 WarnIfSuperuserMixin,
                 DetailView):
    context_object_name = "spec"
    model = Specification
    slug_field = "slug"
    template_name = "tank/spec_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SpecDetail, self).get_context_data(**kwargs)
        context["tank_list"] = Tank.objects.filter(spec=self.object)
        return context


class SpecList(LoginRequiredMixin,
               ConsentRequiredMixin,
               WarnIfSuperuserMixin,
               ListView):
    model = Specification
    context_object_name = "spec_list"
    template_name = "tank/spec_list.html"


class SpecUpdate(LoginRequiredMixin,
                 ConsentRequiredMixin,
                 WarnIfSuperuserMixin,
                 SpecActionMixin,
                 UpdateView):
    '''update Specification info'''
    context_object_name = "spec"
    model = Specification
    slug_field = "slug"
    template_name = "tank/spec_form.html"

    def success_msg(self):
        return "The specification \"{0}\" was updated successfully!".format(self.get_object())

    def cancel_msg(self):
        return "The specification \"{0}\" was not updated!".format(self.get_object())

    def cancel_url(self):
        return self.get_object().get_absolute_url()


class TankActionMixin(AbstractActionMixin):
    '''set a message of a specification is created or saved'''
    fields = (
        "serial_number",
        "owner",
        "code",
        "doubles_code",
        "spec",
        "is_active",
    )


class TankCreate(LoginRequiredMixin,
                 ConsentRequiredMixin,
                 WarnIfSuperuserMixin,
                 TankActionMixin,
                 CreateWithInlinesView):
    '''create a new Tank'''
    model = Tank
    inlines = [HydroInline]

    def success_msg(self):
        form = self.get_form()
        code = form['code'].value()
        return "The tank \"{0}\" was created successfully.".format(code)

    def cancel_msg(self):
        return "The tank was not created!"

    def cancel_url(self):
        return reverse("tank:list")


class TankDetail(LoginRequiredMixin,
                 ConsentRequiredMixin,
                 WarnIfSuperuserMixin,
                 DetailView):
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


class TankList(SortableMixin,
               LoginRequiredMixin,
               ConsentRequiredMixin,
               WarnIfSuperuserMixin,
               ListView):
    model = Tank
    context_object_name = "tank_list"


class TankUpdate(LoginRequiredMixin,
                 ConsentRequiredMixin,
                 WarnIfSuperuserMixin,
                 TankActionMixin,
                 UpdateWithInlinesView):
    '''update Tank info'''
    context_object_name = "tank"
    model = Tank
    slug_field = "code"
    inlines = [HydroInline]

    def success_msg(self):
        return "The tank \"{0}\" was updated successfully.".format(self.get_object())

    def cancel_msg(self):
        return "The tank \"{0}\" was not updated!".format(self.get_object())

    def cancel_url(self):
        return self.get_object().get_absolute_url()


class VipCreate(LoginRequiredMixin,
                ConsentRequiredMixin,
                WarnIfSuperuserMixin,
                AbstractActionMixin,
                CreateView):
    '''create a new Vip'''
    form_class = VipForm
    model = Vip

    def success_msg(self):
        return "The VIP form was created successfully!"

    def cancel_msg(self):
        return "The VIP form was not created!"

    def cancel_url(self):
        return reverse("vip_list")

    def get_context_data(self, **kwargs):
        context = super(VipCreate, self).get_context_data(**kwargs)
        context["tank"] = Tank.objects.get(code=self.kwargs.get("slug"))
        return context


class VipDetail(LoginRequiredMixin,
                ConsentRequiredMixin,
                WarnIfSuperuserMixin,
                DetailView):
    context_object_name = "vip"
    model = Vip
    slug_field = "id"


class VipList(LoginRequiredMixin,
              ConsentRequiredMixin,
              WarnIfSuperuserMixin,
              ListView):
    model = Vip
    context_object_name = "vip_list"

    def get_queryset(self):
        return Vip.objects.current()


class VipUpdate(LoginRequiredMixin,
                ConsentRequiredMixin,
                WarnIfSuperuserMixin,
                AbstractActionMixin,
                UpdateWithInlinesView):
    '''update Vip info'''
    context_object_name = "vip"
    form_class = VipForm
    model = Vip

    def success_msg(self):
        return "The VIP form was updated successfully!"

    def cancel_msg(self):
        return "The VIP form was not updated!"

    def cancel_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(VipUpdate, self).get_context_data(**kwargs)
        vip = Vip.objects.get(id=self.kwargs.get("pk"))
        context["tank"] = Tank.objects.get(id=vip.tank.id)
        return context


@warn_if_superuser
@login_required
@consent_required
def eighteen_step(request):
    ''' A page for filling tanks from the banked gases'''
    return render(request, "tank/eighteen_step.html")
