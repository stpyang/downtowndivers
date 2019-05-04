'''Copyright 2016 DDNY. All Rights Reserved.'''

import json
from datetime import date
from dateutil.relativedelta import relativedelta

from django.urls import reverse

from ddny.test_decorators import test_consent_required, test_login_required
from ddny.test_views import BaseDdnyTestCase
from .models import Event


class TestDdnyCalendarViews(BaseDdnyTestCase):
    '''test ddny_calendar views'''

#    @test_consent_required(path=reverse("ddny_calendar:add_event"))
    @test_login_required(path=reverse("ddny_calendar:add_event"))
    def test_add_event(self):
        '''test the add_event FBV'''
        self.login()
        count = Event.objects.count()
        tomorrow = date.today() + relativedelta(days=1)
        response = self.client.post(
            path=reverse(viewname="ddny_calendar:add_event"),
            data={
                "title": "test_add_event",
                "start_date": date.today().strftime("%Y-%m-%d"),
                "end_date": tomorrow.strftime("%Y-%m-%d"),
            },
            follow=True
        )
        response_json = json.loads(str(response.content, encoding="utf8"))

        self.assertEquals(count + 1, Event.objects.count())
        self.assertTrue(response_json.get("success"))

#    @test_consent_required(path=reverse("ddny_calendar:add_event"))
    @test_login_required(path=reverse("ddny_calendar:add_event"))
    def test_add_event_error(self):
        '''test that we don't add a bad event'''
        self.login()
        count = Event.objects.count()
        tomorrow = date.today() + relativedelta(days=1)
        response = self.client.post(
            path=reverse(viewname="ddny_calendar:add_event"),
            data={
                "title": "test_add_event_error",
                "start_date": tomorrow.strftime("%Y-%m-%d"),
                "end_date": date.today().strftime("%Y-%m-%d"),
            },
        )
        response_json = json.loads(str(response.content, encoding="utf8"))
        self.assertEquals(count, Event.objects.count())
        self.assertFalse(response_json.get("success"))

#    @test_consent_required(path=reverse("ddny_calendar:delete_event"))
    @test_login_required(path=reverse("ddny_calendar:delete_event"))
    def test_delete_event(self):
        '''test the delete_event FBV'''
        self.login()
        tomorrow = date.today() + relativedelta(days=1)
        event = Event.objects.create(
            title="test_delete_event",
            start_date=date.today().strftime("%Y-%m-%d"),
            end_date=tomorrow.strftime("%Y-%m-%d"),
            member=self.member,
        )
        count = Event.objects.count()
        response = self.client.post(
            path=reverse(viewname="ddny_calendar:delete_event"),
            data={"id": event.id},
            follow=True,
        )
        response_json = json.loads(str(response.content, encoding="utf8"))

        self.assertEquals(count - 1, Event.objects.count())
        self.assertTrue(response_json.get("success"))

#    @test_consent_required(path=reverse("ddny_calendar:delete_event"))
    @test_login_required(path=reverse("ddny_calendar:delete_event"))
    def test_delete_event_error(self):
        '''test that we delete an event that exists'''
        self.login()
        tomorrow = date.today() + relativedelta(days=1)
        event = Event.objects.create(
            title="test_delete_event_error",
            start_date=date.today().strftime("%Y-%m-%d"),
            end_date=tomorrow.strftime("%Y-%m-%d"),
            member=self.member,
        )
        count = Event.objects.count()
        response = self.client.post(
            path=reverse(viewname="ddny_calendar:delete_event"),
            data={"id": event.id + 1},
        )
        response_json = json.loads(str(response.content, encoding="utf8"))

        self.assertEquals(count, Event.objects.count())
        self.assertFalse(response_json.get("success"))

#    @test_consent_required(path=reverse("ddny_calendar:update_event"))
    @test_login_required(path=reverse("ddny_calendar:update_event"))
    def test_update_event(self):
        '''test the update_event FBV'''
        self.login()
        yesterday = date.today() - relativedelta(days=1)
        tomorrow = date.today() + relativedelta(days=1)
        event_before = Event.objects.create(
            title="test_update_event_before",
            start_date=yesterday.strftime("%Y-%m-%d"),
            end_date=date.today().strftime("%Y-%m-%d"),
            member=self.member,
        )
        event_id = event_before.id
        count = Event.objects.count()
        response = self.client.post(
            path=reverse(viewname="ddny_calendar:update_event"),
            data={
                "id": event_id,
                "title": "test_update_event_after",
                "start_date": date.today().strftime("%Y-%m-%d"),
                "end_date": tomorrow.strftime("%Y-%m-%d"),
            },
            follow=True
        )
        response_json = json.loads(str(response.content, encoding="utf8"))
        event_after = Event.objects.get(id=event_id)

        self.assertEquals(count, Event.objects.count())
        self.assertTrue(response_json.get("success"))
        self.assertEquals(event_after.title, "test_update_event_after")
        self.assertEquals(event_after.start_date, date.today())
        self.assertEquals(event_after.end_date, tomorrow)

#    @test_consent_required(path=reverse("ddny_calendar:update_event"))
    @test_login_required(path=reverse("ddny_calendar:update_event"))
    def test_update_event_error(self):
        '''test that we don't update with bad data'''
        self.login()
        yesterday = date.today() - relativedelta(days=1)
        tomorrow = date.today() + relativedelta(days=1)
        event_before = Event.objects.create(
            title="test_update_event_before",
            start_date=yesterday.strftime("%Y-%m-%d"),
            end_date=date.today().strftime("%Y-%m-%d"),
            member=self.member
        )
        event_id = event_before.id
        response = self.client.post(
            path=reverse(viewname="ddny_calendar:update_event"),
            data={
                "id": event_id + 1,
                "title": "test_update_event_error",
                "start_date": date.today().strftime("%Y-%m-%d"),
                "end_date": tomorrow.strftime("%Y-%m-%d"),
            },
        )
        response_json = json.loads(str(response.content, encoding="utf8"))
        self.assertFalse(response_json.get("success"))

        response = self.client.post(
            path=reverse(viewname="ddny_calendar:update_event"),
            data={
                "id": event_id,
                "title": "test_update_event_error",
                "start_date": tomorrow.strftime("%Y-%m-%d"),
                "end_date": date.today().strftime("%Y-%m-%d"),
            },
        )
        response_json = json.loads(str(response.content, encoding="utf8"))
        self.assertFalse(response_json.get("success"))

