'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel

from registration.models import Member

class Event(TimeStampedModel):
    title = models.CharField(max_length=40)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    member = models.ForeignKey(Member, blank=True, null=True)

    def get_absolute_url(self): # pylint: disable=no-self-use
        return reverse("home")

    def clean(self):
        super(Event, self).clean()
        if self.start_date > self.end_date:
            raise ValidationError("Event must start before it ends")
