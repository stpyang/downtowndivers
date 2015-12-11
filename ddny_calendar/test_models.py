'''Copyright 2016 DDNY. All Rights Reserved.'''

from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import SimpleTestCase

from .models import Event
from registration.factory import MemberFactory

class TestEventModel(SimpleTestCase):
    '''test event transaction model'''

    def test_bad_dates(self):
        with self.assertRaises(ValidationError):
            member = MemberFactory.create()
            event = Event.objects.create(
                title="Test Title",
                start_date=date.today(),
                end_date=date.today() - relativedelta(days=1),
                member=member
            )
            event.clean()

    def test_absolute_url(self):
        member = MemberFactory.create()
        event = Event.objects.create(
            title="Test Title",
            start_date=date.today(),
            end_date=date.today() + relativedelta(days=1),
            member=member
        )
        self.assertEquals(event.get_absolute_url(), reverse("home"))
