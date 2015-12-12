'''Copyright 2016 DDNY. All Rights Reserved.'''

from dateutil.relativedelta import relativedelta

from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel

from registration.models import Member

class Event(TimeStampedModel):
    '''Stuff which goes on the calendar'''
    class Meta:
        ordering = ("start_date",)

    title = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()
    member = models.ForeignKey(Member)
    show_on_homepage = models.NullBooleanField(default=False)

    def get_absolute_url(self): # pylint: disable=no-self-use
        return reverse("home")

    def clean(self):
        super(Event, self).clean()
        if self.start_date >= self.end_date:
            raise ValidationError("Event must start before it ends")

    def get_dates(self):
        if self.start_date + relativedelta(days=1) == self.end_date:
            return self.start_date.strftime("%Y-%m-%d")
        else:
            end_date = self.end_date - relativedelta(seconds = 1)
            return "{0} to {1}".format(
                self.start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )


    def __str__(self):
        return "{0} {1}".format(self.get_dates(), self.title)
