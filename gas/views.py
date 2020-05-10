'''Copyright 2016 DDNY New York. All Rights Reserved.'''

from braces.views import LoginRequiredMixin

from django.views.generic import DetailView, ListView

from ddny.mixins import ConsentRequiredMixin, WarnIfSuperuserMixin
from ddny.settings import prices
from .models import Gas


class GasDetail(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, DetailView):
    '''https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#detailview'''

    context_object_name = 'gas'
    model = Gas
    slug_field = 'slug'


class GasList(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, ListView):
    '''https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#listview'''

    model = Gas
    context_object_name = 'gas_list'

    def get_context_data(self, **kwargs):
        context = super(GasList, self).get_context_data(**kwargs)
        context['equipment_cost_fixed'] = prices.EQUIPMENT_COST_FIXED
        context['equipment_cost_proportional'] = prices.EQUIPMENT_COST_PROPORTIONAL
        return context
