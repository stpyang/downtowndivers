'''Copyright 2016 DDNY. All Rights Reserved.'''

#Sorry, I have to do something rather gross in order to make django-ical
#compatible with v1.8 on python 3. See the un-pulled fix at this link below:
#https://bitbucket.org/IanLewis/django-ical/pull-requests/6/updated-code-and-tests-to-support-python-3/diff # pylint: disable=line-too-long

#Views for generating ical feeds.
#TODO(stpyang: Remove this when django-ical gets updated.

from datetime import datetime
from calendar import timegm

from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.views import Feed
from django.utils.http import http_date
import six

from django_ical import feedgenerator


__all__ = (
    'ICalFeed',
)

# Extra fields added to the Feed object
# to support ical
FEED_EXTRA_FIELDS = (
    'method',
    'product_id',
    'timezone',
)
# Extra fields added to items (events) to
# support ical
ICAL_EXTRA_FIELDS = (
    'timestamp',        # dtstamp
    'created',          # created
    'modified',         # last-modified
    'start_datetime',   # dtstart
    'end_datetime',     # dtend
    'transparency',     # transp
    'location',         # location
    'geolocation',      # latitude;longitude
    'organizer',        # email, cn, and role
)


class ICalFeed(Feed):
    """
    iCalendar Feed

    Existing Django syndication feeds

    :title: X-WR-CALNAME
    :description: X-WR-CALDESC
    :item_guid: UID
    :item_title: SUMMARY
    :item_description: DESCRIPTION
    :item_link: URL

    Extension fields

    :method: METHOD
    :timezone: X-WR-TIMEZONE
    :item_class: CLASS
    :item_timestamp: DTSTAMP
    :item_created: CREATED
    :item_modified: LAST-MODIFIED
    :item_start_datetime: DTSTART
    :item_end_datetime: DTEND
    :item_transparency: TRANSP
    """
    feed_type = feedgenerator.DefaultFeed

    def __call__(self, request, *args, **kwargs):
        """
        Copied from django.contrib.syndication.views.Feed

        Supports file_name as a dynamic attr.
        """
        try:
            obj = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404('Feed object does not exist.')
        feedgen = self.get_feed(obj, request)
        response = HttpResponse(content_type=feedgen.mime_type)
        if hasattr(self, 'item_pubdate') or hasattr(self, 'item_updateddate'):
            # if item_pubdate or item_updateddate is defined for the feed, set
            # header so as ConditionalGetMiddleware is able to send 304 NOT MODIFIED
            response['Last-Modified'] = http_date(
                timegm(feedgen.latest_post_date().utctimetuple()))
        feedgen.write(response, 'utf-8')

        filename = self._get_dynamic_attr('file_name', obj)
        if filename:
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename

        return response

    def _get_dynamic_attr(self, attname, obj, default=None):
        """
        Copied from django.contrib.syndication.views.Feed (v1.7.1)
        """
        try:
            attr = getattr(self, attname)
        except AttributeError:
            return default
        if callable(attr):
            # Check co_argcount rather than try/excepting the function and
            # catching the TypeError, because something inside the function
            # may raise the TypeError. This technique is more accurate.
            try:
                code = six.get_function_code(attr)
            except AttributeError:
                code = six.get_function_code(attr.__call__)
            if code.co_argcount == 2:       # one argument is 'self'
                return attr(obj)
            else:
                return attr()
        return attr

    # NOTE: Not used by icalendar but required
    #       by the Django syndication framework.
    link = ''

    def method(self, obj): # pylint: disable=no-self-use,unused-argument
        return 'PUBLISH'

    def feed_extra_kwargs(self, obj):
        kwargs = {}
        for field in FEED_EXTRA_FIELDS:
            val = self._get_dynamic_attr(field, obj)
            if val:
                kwargs[field] = val
        return kwargs

    def item_timestamp(self, obj): # pylint: disable=no-self-use,unused-argument
        return datetime.now()

    def item_extra_kwargs(self, obj):
        kwargs = {}
        for field in ICAL_EXTRA_FIELDS:
            val = self._get_dynamic_attr('item_' + field, obj)
            if val:
                kwargs[field] = val
        return kwargs


################################################################################
# This is where my code starts

import json
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
# from django.core.exceptions import ObjectDoesNotExist, ValidationError
# from django.http import HttpResponse
# from django_ical.views import ICalFeed # fixed above
from django.views.decorators.csrf import csrf_exempt

from .models import Event
from ddny.decorators import consent_required


@csrf_exempt
@login_required
#@consent_required
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
        return HttpResponse(
            json.dumps({"id": event.id, "success": True}),
            content_type="application/json"
        )
    except ValidationError as e:
        return HttpResponse(
            json.dumps({"success": False, "error": str(e)}),
            content_type="application/json"
        )


@csrf_exempt
@login_required
#@consent_required
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
        return HttpResponse(
            json.dumps({"id": event.id, "success": True}),
            content_type="application/json"
        )
    except (ObjectDoesNotExist, ValidationError) as e:
        return HttpResponse(
            json.dumps({"success": False, "error": str(e)}),
            content_type="application/json"
        )

@csrf_exempt
@login_required
#@consent_required
def delete_event(request):
    try:
        event = Event.objects.get(id=request.POST.get("id"))
        event.delete()
        return HttpResponse(
            json.dumps({"success": True}),
            content_type="application/json"
        )
    except ObjectDoesNotExist as e:
        return HttpResponse(
            json.dumps({"success": False, "error": str(e)}),
            content_type="application/json"
        )


class EventFeed(ICalFeed):
    """
    A simple event calender
    """
    product_id = "DDNY"
    timezone = "UTC"
    file_name = "ddny_events.ics"

    def items(self): # pylint: disable=no-self-use
        return Event.objects.all().order_by('-start_date')

    def item_title(self, item): # pylint: disable=no-self-use
        return item.title

    def item_start_datetime(self, item): # pylint: disable=no-self-use
        return item.start_date

    def item_datetime(self, item): # pylint: disable=no-self-use
        return item.end_date + relativedelta(days=1)
