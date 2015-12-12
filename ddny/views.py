'''Copyright 2016 DDNY. All Rights Reserved.'''

from datetime import date

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template

from .decorators import consent_required, warn_if_superuser
from ddny_calendar.models import Event


class AbstractActionMixin(object):
    '''set a message of if an object is created or saved'''

    @property
    def success_msg(self): # pragma: no cover pylint: disable=no-self-use
        return NotImplemented

    @property
    def cancel_msg(self): # pragma: no cover pylint: disable=no-self-use
        return NotImplemented

    @property
    def cancel_url(self): # pragma: no cover pylint: disable=no-self-use
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg())
        return super(AbstractActionMixin, self).form_valid(form)

    def forms_valid(self, forms, inlines):
        messages.info(self.request, self.success_msg())
        return super(AbstractActionMixin, self).forms_valid(forms, inlines)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            messages.warning(self.request, self.cancel_msg())
            return HttpResponseRedirect(self.cancel_url())
        else:
            return super(AbstractActionMixin, self).post(request, *args, **kwargs)


def contact_info(request):
    return render(request, "ddny/contact_info.html")


def club_dues(request):
    return render(request, "ddny/club_dues.html")


@warn_if_superuser
@login_required
@consent_required
def home(request):
    '''A copy of the home screen that contains the first version of the ddny calendar'''
    event_array = map(
        lambda event: {
            "id": event.id,
            "title": event.title,
            "start": event.start_date.strftime("%Y-%m-%d"),
            "end": event.end_date.strftime("%Y-%m-%d"),
        },
        Event.objects.all()
    )

    upcoming_event_array = Event.objects.filter(show_on_homepage=True, start_date__gte=date.today())
    upcoming_events = map(
        lambda event: {
            "dates": event.get_dates(),
            "title": event.title,
        },
        upcoming_event_array,
    )
    upcoming_event_ids = map(
        lambda event: event.id,
        upcoming_event_array,
    )

    context = {
        "event_array": list(event_array),
        "upcoming_events": upcoming_events,
        "upcoming_event_ids": list(upcoming_event_ids),
        "add_event": reverse("ddny_calendar:add_event"),
        "delete_event": reverse("ddny_calendar:delete_event"),
        "update_event": reverse("ddny_calendar:update_event"),
    }
    return render(request, "ddny/home.html", context)


def privacy_policy(request):
    return render(request, "ddny/privacy_policy.html")


def refund_policy(request):
    return render(request, "ddny/refund_policy.html")


def oops(request, text_template, html_template, view, error_messages):
    '''In exceptional cases (no pun intended) send an e-mail'''
    context = {
        "oops_email": settings.OOPS_EMAIL,
        "current_user": request.user.username,
        "error_messages": error_messages,
    }
    text_content = get_template(text_template)
    html_content = get_template(html_template)
    warning = EmailMultiAlternatives(
        subject="DDNY automated warning: {0}".format(view),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.OOPS_EMAIL],
        body=text_content.render(context)
    )
    warning.attach_alternative(
        content=html_content.render(context),
        mimetype="text/html",
    )
    warning.send()
    return render(request, "ddny/oops.html", context)

