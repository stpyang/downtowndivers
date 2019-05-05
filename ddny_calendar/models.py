'''Copyright 2016 DDNY. All Rights Reserved.'''

from dateutil.relativedelta import relativedelta

from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from model_utils.models import TimeStampedModel

from registration.models import Member


class Event(TimeStampedModel):
    '''Stuff which goes on the calendar'''
    class Meta:
        ordering = ("start_date", "end_date")

    title = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    show_on_homepage = models.NullBooleanField(default=False)

    def get_absolute_url(self): # pylint: disable=no-self-use
        return reverse("home")

    def clean(self):
        super(Event, self).clean()
        if self.start_date > self.end_date:
            raise ValidationError("Event must start before it ends")

    # date are iclusive
    def get_dates(self):
        if self.start_date == self.end_date - relativedelta(days=1):
            return self.start_date.strftime("%Y-%m-%d")
        return "{0} to {1}".format(
            self.start_date.strftime("%Y-%m-%d"),
            (self.end_date - relativedelta(days=1)).strftime("%Y-%m-%d"),
        )


    def __str__(self):
        return "{0} {1}".format(self.get_dates(), self.title)
