'''Copyright 2016 DDNY. All Rights Reserved.'''

from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.urls import reverse

from .models import Event
from registration.factory import MemberFactory

class TestEventModel(SimpleTestCase):
    '''test event transaction model'''

    def test_event_stringify(self):
        '''test that the stringify method for the Event model still works'''
        member = MemberFactory.create()
        event = Event.objects.create(
            title="test_event_stringify",
            start_date=date.today(),
            end_date=date.today() + relativedelta(days=1),
            member=member,
        )
        self.assertEquals(str(event), "{0} {1}".format(
            date.today().strftime("%Y-%m-%d"),
            "test_event_stringify"
        ))
        event = Event.objects.create(
            title="test_event_stringify",
            start_date=date.today(),
            end_date=date.today() + relativedelta(days=2),
            member=member,
        )
        self.assertEquals(str(event), "{0} to {1} {2}".format(
            date.today().strftime("%Y-%m-%d"),
            (date.today() + relativedelta(days=1)).strftime("%Y-%m-%d"),
            "test_event_stringify"
        ))

    def test_bad_dates(self):
        with self.assertRaises(ValidationError):
            member = MemberFactory.create()
            event = Event.objects.create(
                title="test_bad_dates",
                start_date=date.today(),
                end_date=date.today() - relativedelta(days=1),
                member=member
            )
            event.clean()

    def test_absolute_url(self):
        member = MemberFactory.create()
        event = Event.objects.create(
            title="test_absolute_url",
            start_date=date.today(),
            end_date=date.today() + relativedelta(days=1),
            member=member
        )
        self.assertEquals(event.get_absolute_url(), reverse("home"))

    def test_get_dates(self):
        '''test that the get_dates for the Event model works'''
        member = MemberFactory.create()
        event = Event.objects.create(
            title="test_get_dates",
            start_date=date.today(),
            end_date=date.today() + relativedelta(days=1),
            member=member,
        )
        self.assertEquals(event.get_dates(), "{0}".format(date.today().strftime("%Y-%m-%d")))
        event = Event.objects.create(
            title="test_get_dates",
            start_date=date.today(),
            end_date=date.today() + relativedelta(days=2),
            member=member,
        )
        self.assertEquals(event.get_dates(), "{0} to {1}".format(
            date.today().strftime("%Y-%m-%d"),
            (date.today() + relativedelta(days=1)).strftime("%Y-%m-%d"),
        ))
