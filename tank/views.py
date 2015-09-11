'''Copyright 2015 DDNY New York. All Rights Reserved.'''

from braces.views import LoginRequiredMixin
from extra_views import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView

from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ddny.mixins import ConsentRequiredMixin, WarnIfSuperuserMixin
from ddny.views import AbstractActionMixin
from .models import Hydro, Specification, Tank, Vip


class HydroInline(InlineFormSet):
    model = Hydro
    extra = 1


class VipInline(InlineFormSet):
    model = Vip
    extra = 1


class SpecActionMixin(AbstractActionMixin):
    '''set a message of a specification is created or saved'''
    fields = (
        "name",
        "metal",
        "volume",
        "pressure",
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
    inlines = [HydroInline, VipInline]

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
        context['hydros'] = Hydro.objects.filter(tank=self.object)
        context['vips'] = Vip.objects.filter(tank=self.object)
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
    inlines = [HydroInline, VipInline]

    def success_msg(self):
        return "The tank \"{0}\" was updated successfully.".format(self.object.code)
