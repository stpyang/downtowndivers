'''Copyright 2016 DDNY. All Rights Reserved.'''

from braces.views import LoginRequiredMixin
from collections import defaultdict
import braintree
import csv
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.html import escape
from django.utils.text import slugify
from django.views.generic import ListView

from ddny.core import cash
from ddny.decorators import consent_required, warn_if_superuser
from ddny.mixins import ConsentRequiredMixin, WarnIfSuperuserMixin
from ddny.views import oops, __calculate_prepaid
from gas.models import Gas
from registration.models import Member
from tank.models import Tank
from .emails import TankWarningEmail
from .models import _build_fill, Fill, Prepay
from .forms import BillToForm, BlendForm, FillForm


def __gas_info():
    '''helper function for the blend and pay views'''
    gas_info = {}
    for gas in Gas.objects.all():
        gas_dict = {
            "oxygen_percentage": float(gas.oxygen_percentage),
            "helium_percentage": float(gas.helium_percentage),
            "oxygen_fraction": float(gas.oxygen_fraction),
            "helium_fraction": float(gas.helium_fraction),
            "cost": float(gas.cost),
            "name": gas.name,
        }
        gas_info[gas.slug] = gas_dict
    return gas_info


def __tank_info():
    '''helper function for the blend and pay views'''
    tank_info = defaultdict(list)
    for tank in Tank.objects.all():
        tank_dict = {
            "is_current_hydro": tank.is_current_hydro,
            "is_current_vip": tank.is_current_vip,
            "last_hydro_date": "None",
            "last_vip_date": "None",
            "tank_code": escape(tank.code),
            "tank_factor": tank.tank_factor,
        }
        if tank.last_hydro:
            tank_dict["last_hydro_date"] = str(tank.last_hydro.date)
        if tank.last_vip:
            tank_dict["last_vip_date"] = str(tank.last_vip.date)
        if tank.doubles_code:
            tank_info[escape(tank.doubles_code)] += [tank_dict]
        else:
            tank_info[escape(tank.code)] += [tank_dict]
    return tank_info


@warn_if_superuser
@login_required
@consent_required
def prepay(request):
    '''members pay their fillstation balances'''
    if braintree.Configuration.environment == braintree.Environment.Sandbox:
        messages.warning(
            request,
            "Payments are connected to braintree sandbox!"
        )
    context = {
        "braintree_client_token": settings.BRAINTREE_CLIENT_TOKEN,
    }
    return render(request, "fillstation/prepay.html", context)


class FillLog(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, ListView):
    model = Fill
    context_object_name = "fill_log"
    template_name = "fillstation/log.html"

    def get_queryset(self):
        return Fill.objects.all()[:75]


class PayFills(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, ListView):
    '''class based view which lists unpaid fills by user'''
    model = Fill
    context_object_name = "fill_log"
    template_name = "fillstation/pay_fills.html"

    def get_context_data(self, **kwargs):
        context = super(PayFills, self).get_context_data(**kwargs)
        context["braintree_client_token"] = settings.BRAINTREE_CLIENT_TOKEN
        if self.request.user.username == "fillstation":
            context["form"] = BillToForm()
        return context

    def get_queryset(self):
        slug = self.kwargs["slug"]
        if self.request.user.username == "fillstation" and \
            slug == "fillstation":
            return Fill.objects.none()
        elif self.request.user.username == "fillstation" or \
            slugify(self.request.user.username) == slug:
            member = get_object_or_404(Member, slug=slug)
            return Fill.objects.unpaid() \
                .filter(bill_to=member)
        else:
            raise PermissionDenied

    def dispatch(self, *args, **kwargs):
        if braintree.Configuration.environment == braintree.Environment.Sandbox:
            messages.warning(
                self.request,
                "Payments are connected to braintree sandbox!"
            )
        return super(PayFills, self).dispatch(*args, **kwargs)


@warn_if_superuser
@login_required
@consent_required
def blend(request):
    '''A page for partial pressure blending'''
    form = BlendForm(
        user=request.user,
        initial={
            "blender": request.user.username,
            "bill_to": request.user.username,
        })
    context = {
        "tank_nazi": settings.TANK_NAZI,
        "equipment_cost_fixed": settings.EQUIPMENT_COST_FIXED,
        "equipment_cost_proportional": settings.EQUIPMENT_COST_PROPORTIONAL,
        "form": form,
        "gas_info": json.dumps(__gas_info()),
        "tank_info": json.dumps(__tank_info()),
    }

    return render(request, "fillstation/blend.html", context)


@login_required
@consent_required
def download(request): # pylint: disable=unused-argument
    "Download entire fill log in a csv file"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename='fill_log.csv'"

    writer = csv.writer(response)
    fields = Fill._meta.fields # pylint: disable=W0212
    writer.writerow([field.name for field in fields])
    for f in Fill.objects.all():
        writer.writerow([str(getattr(f, field.name)) for field in fields])

    return response


@warn_if_superuser
@login_required
@consent_required
def fill(request):
    ''' A page for filling tanks from the banked gases'''
    form = FillForm(
        user=request.user,
        initial={
            "blender": request.user.username,
            "bill_to": request.user.username,
        })
    context = {
        "tank_nazi": settings.TANK_NAZI,
        "equipment_cost_fixed": settings.EQUIPMENT_COST_FIXED,
        "equipment_cost_proportional": settings.EQUIPMENT_COST_PROPORTIONAL,
        "form": form,
        "gas_info": json.dumps(__gas_info()),
        "tank_info": json.dumps(__tank_info())
    }

    return render(request, "fillstation/fill.html", context)


@warn_if_superuser
@login_required
@consent_required
def log_fill(request):
    '''
    Add a fill to the database.
    The request must contain a json object with seven fields specified below.
    Send warning emails if the tank has no current hydro/vip
    '''
    if request.method == "POST":
        try:
            num_rows = request.POST.get("num_rows", 0)
            num_rows = int(num_rows)

            tank_warnings = {}

            total_volume = defaultdict(float) # indexed by tank_code
            fills = list()

            for i in range(0, num_rows):
                blender = request.POST.get("blender_{0}".format(i))
                bill_to = request.POST.get("bill_to_{0}".format(i))
                tank_code = request.POST.get("tank_code_{0}".format(i))
                gas_name = request.POST.get("gas_name_{0}".format(i))
                psi_start = request.POST.get("psi_start_{0}".format(i))
                psi_end = request.POST.get("psi_end_{0}".format(i))
                total_price = request.POST.get("total_price_{0}".format(i))
                is_equipment_surcharge = request.POST.get("is_equipment_surcharge_{0}".format(i))
                is_blend = request.POST.get("is_blend_{0}".format(i))

                blender = get_object_or_404(Member, username=blender)
                bill_to = get_object_or_404(Member, username=bill_to)
                tank = get_object_or_404(Tank, code=tank_code)

                psi_start = int(psi_start)
                psi_end = int(psi_end)
                total_price = cash(total_price)
                is_blend = is_blend.lower() == "true"

                if type(is_equipment_surcharge) is str:
                    is_equipment_surcharge = is_equipment_surcharge.lower() == "true"
                if type(is_blend) is str:
                    is_blend = is_blend.lower() == "true"

                tank_factor = tank.tank_factor
                cubic_feet = float(psi_end - psi_start) * tank.tank_factor / 100.0
                if not is_equipment_surcharge:
                    total_volume[(blender, bill_to, tank_code)] = total_volume[(blender, bill_to, tank_code)] + cubic_feet

                warning = tank_warnings.get(blender)
                if warning == None:
                    warning = TankWarningEmail(blender=blender.email)
                if not tank.is_current_hydro:
                    service = "hydro"
                    service_date = str(tank.last_hydro.date) if tank.last_hydro else None
                    warning.add(
                        tank_code=tank.code,
                        psi_start=psi_start,
                        psi_end=psi_end,
                        gas_name=gas_name,
                        service=service,
                        service_date=service_date,
                    )
                    tank_warnings[blender] = warning

                if not tank.is_current_vip:
                    service = "vip"
                    service_date = str(tank.last_vip.date) if tank.last_vip else None
                    warning.add(
                        tank_code=tank.code,
                        psi_start=psi_start,
                        psi_end=psi_end,
                        gas_name=gas_name,
                        service=service,
                        service_date=service_date,
                    )
                    tank_warnings[blender] = warning

                new_fill = _build_fill(
                    username=request.user.username,
                    blender=blender,
                    bill_to=bill_to,
                    tank_code=tank.code,
                    gas_name=gas_name,
                    psi_start=psi_start,
                    psi_end=psi_end,
                    is_equipment_surcharge=is_equipment_surcharge,
                    is_blend=is_blend,
                )

                if not is_equipment_surcharge and total_price != new_fill.total_price:
                    gas = get_object_or_404(Gas, name=gas_name)
                    raise SuspiciousOperation(
                        "Price verification failure. ({0} != {1})".format(
                            total_price, new_fill.total_price
                        )
                    )

                fills.append(new_fill)

            # TODO(stpyang): make this functional
            equipment_surcharge_verification = 0
            for cubic_feet in total_volume.values():
                equipment_surcharge_verification = equipment_surcharge_verification + cash(
                    float(settings.EQUIPMENT_COST_FIXED) + cubic_feet * float(settings.EQUIPMENT_COST_PROPORTIONAL)
                )
            equipment_surcharge_total = 0
            for fill in fills:
                if fill.is_equipment_surcharge:
                    equipment_surcharge_total = equipment_surcharge_total + fill.total_price

            if not equipment_surcharge_verification == equipment_surcharge_total:
                raise SuspiciousOperation(
                    "Price verification failure. ({0} != {1})".format(
                        equipment_surcharge_verification, equipment_surcharge_total
                    )
                )

            # I have to save here, or else I cannot create a related Prepay object
            for fill in fills:
                fill.save()

            prepaid_balance = __calculate_prepaid(bill_to)

            if (prepaid_balance):
                for fill in Fill.objects.unpaid().filter(bill_to__username=bill_to):
                    if prepaid_balance >= fill.total_price:
                        fill.is_paid = True
                        fill.save()
                        Prepay.objects.create(
                            member=bill_to,
                            amount=-fill.total_price,
                            fill=fill,
                            is_paid=True,
                        )
                        prepaid_balance = prepaid_balance - fill.total_price

            for w in tank_warnings.values():
                w.send()

            return render(request, "fillstation/fill_success.html")
        except SuspiciousOperation as e:
            return oops(
                request=request,
                text_template="fillstation/log_fill_warning.txt",
                html_template="fillstation/log_fill_warning.html",
                view="log_fill",
                error_messages=e.args,
            )
