'''Copyright 2016 DDNY New York. All Rights Reserved.'''

from braces.views import LoginRequiredMixin

from django.conf import settings
from django.views.generic import DetailView, ListView

from ddny.mixins import ConsentRequiredMixin, WarnIfSuperuserMixin
from .models import Gas


class GasDetail(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, DetailView):
    context_object_name = "gas"
    model = Gas
    slug_field = "slug"


class GasList(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, ListView):
    model = Gas
    context_object_name = "gas_list"

    def get_context_data(self):
        context = super(GasList, self).get_context_data()
        context["equipment_cost"] = settings.EQUIPMENT_COST
        return context
