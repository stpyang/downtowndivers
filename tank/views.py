
'''Copyright 2015 DDNY New York. All Rights Reserved.'''

from braces.views import LoginRequiredMixin
from extra_views import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView

from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ddny.decorators import consent_required, warn_if_superuser
from ddny.mixins import ConsentRequiredMixin, WarnIfSuperuserMixin
from django.shortcuts import render
from ddny.views import AbstractActionMixin
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
    model = Specification
    template_name = "tank/spec_form.html"

    def success_msg(self):
        form = self.get_form()
        name = form['name'].value()
        return "The specification \"{0}\" was created successfully.".format(name)


class SpecDetail(LoginRequiredMixin,
                 ConsentRequiredMixin,
                 WarnIfSuperuserMixin,
                 DetailView):
    context_object_name = "spec"
    model = Specification
    slug_field = "slug"
    template_name = "tank/spec_detail.html"


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
    context_object_name = "spec"
    model = Specification
    slug_field = "slug"
    template_name = "tank/spec_form.html"

    def success_msg(self):
        return "The specification \"{0}\" was updated successfully.".format(self.object)


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
    model = Tank
    inlines = [HydroInline]

    def success_msg(self):
        form = self.get_form()
        code = form['code'].value()
        return "The tank \"{0}\" was created successfully.".format(code)


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
        return context


class TankList(LoginRequiredMixin,
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
    context_object_name = "tank"
    model = Tank
    slug_field = "code"
    inlines = [HydroInline]

    def success_msg(self):
        return "The tank \"{0}\" was updated successfully.".format(self.object.code)


class VipCreate(LoginRequiredMixin,
                ConsentRequiredMixin,
                WarnIfSuperuserMixin,
                AbstractActionMixin,
                CreateView):
    form_class = VipForm
    model = Vip

    def success_msg(self):
        return "The VIP form was created successfully!"

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


class VipUpdate(LoginRequiredMixin,
                ConsentRequiredMixin,
                WarnIfSuperuserMixin,
                AbstractActionMixin,
                UpdateWithInlinesView):
    context_object_name = "vip"
    form_class = VipForm
    model = Vip

    def success_msg(self):
        return "The VIP form was updated successfully!"

    def get_context_data(self, **kwargs):
        context = super(VipUpdate, self).get_context_data(**kwargs)
        context["tank"] = Tank.objects.get(id=self.kwargs.get("pk"))
        return context


@warn_if_superuser
@login_required
@consent_required
def eighteen_step(request):
    ''' A page for filling tanks from the banked gases'''
    return render(request, "tank/eighteen_step.html")
