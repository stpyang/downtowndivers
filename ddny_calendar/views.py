'''Copyright 2020 DDNY. All Rights Reserved.'''

from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ical.views import ICalFeed

from ddny.decorators import consent_required
from .models import Event


@csrf_exempt
@consent_required
@login_required
def add_event(request):
    try:
        event = Event(
            title=request.POST.get("title"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            member=request.user.member,
            show_on_homepage=request.POST.get("show_on_homepage")
        )
        event.clean()
        event.save()
        return JsonResponse({"id": event.id, "success": True})
    except ValidationError as exception:
        return JsonResponse({"success": False, "error": str(exception)})


@csrf_exempt
@consent_required
@login_required
def update_event(request):
    try:
        event = Event.objects.get(id=request.POST.get("id"))
        event.title = request.POST.get("title")
        event.start_date = request.POST.get("start_date")
        event.end_date = request.POST.get("end_date")
        event.member = request.user.member
        event.show_on_homepage = request.POST.get("show_on_homepage")
        event.clean()
        event.save()
        return JsonResponse({"id": event.id, "success": True})
    except (ObjectDoesNotExist, ValidationError) as exception:
        return JsonResponse({"success": False, "error": str(exception)})


@csrf_exempt
@consent_required
@login_required
def delete_event(request):
    try:
        event = Event.objects.get(id=request.POST.get("id"))
        event.delete()
        return JsonResponse({"success": True})
    except ObjectDoesNotExist as exception:
        return JsonResponse({"success": False, "error": str(exception)})


class EventFeed(ICalFeed):
    """
    A simple event calender
    """
    product_id = "DDNY"
    timezone = "UTC"
    file_name = "ddny_events.ics"

    def items(self):  # pylint: disable=no-self-use
        return Event.objects.all().order_by('-start_date')

    def item_title(self, item):  # pylint: disable=no-self-use
        return item.title

    def item_start_datetime(self, item):  # pylint: disable=no-self-use
        return item.start_date

    def item_datetime(self, item):  # pylint: disable=no-self-use
        return item.end_date + relativedelta(days=1)
