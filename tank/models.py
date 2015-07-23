'''Copyright 2015 DDNY. All Rights Reserved.'''

from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import smart_text
from django.utils.text import slugify

from model_utils.models import TimeStampedModel

from registration.models import Member


class Specification(TimeStampedModel):
    '''manufacturing specifications for tanks'''

    class Meta:
        ordering = ("name", )

    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(null=False, blank=True, unique=True)
    metal = models.CharField(
        max_length=8,
        choices=(
            ('Al', 'Aluminum'),
            ('St', 'Steel'),
        ),
        default='Al',
    )
    volume = models.FloatField()  # cubic feet only
    pressure = models.PositiveSmallIntegerField()  # psi only

    @property
    def tank_factor(self):
        return 100.0 * self.volume / self.pressure

    def get_absolute_url(self):
        return reverse("tank:spec_detail", kwargs={"slug": self.slug})

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(Specification, self).save(kwargs)

    def __str__(self):
        return smart_text(self.name)


class TankManager(models.Manager):

    def __init__(self):
        super(TankManager, self).__init__()

    def active(self, **kwargs):
        return self.filter(is_active=True, **kwargs)


class Tank(TimeStampedModel):
    '''tanks owned by ddny members'''

    class Meta:
        ordering = ("owner__username", "code",)

    objects = TankManager()

    serial_number = models.SlugField(null=False, unique=True)
    owner = models.ForeignKey(Member, null=False)
    code = models.SlugField(
        help_text="Required. 50 characters or fewer.\
            Letters, numbers, underscores, and hyphens only.  Must be unique.",
        null=False,
        unique=True,
    )
    doubles_code = models.SlugField(
        blank=True,
        default="",
        help_text="Optional. 50 characters or fewer.\
            Letters, numbers, underscores, and hyphens only. \
            Max two tanks per doubles code.",
    )
    spec = models.ForeignKey(Specification)
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active. \
            Unselect this instead of deleting tanks.",
        verbose_name="Active",
    )

    @property
    def tank_factor(self):
        return self.spec.tank_factor

    @property
    def last_hydro(self):
        date_max = Hydro.objects.filter(tank=self).aggregate(models.Max("date"))
        if date_max:
            return date_max["date__max"]

    @property
    def last_vip(self):
        date_max = Vip.objects.filter(tank=self).aggregate(models.Max("date"))
        if date_max:
            return date_max["date__max"]

    @property
    def current_hydro(self):
        return Hydro.objects.current().filter(tank=self).count() > 0

    @property
    def current_vip(self):
        return Vip.objects.current().filter(tank=self).count() > 0

    def clean(self):
        others = (
            Tank.objects
            .exclude(doubles_code="")
            .exclude(id=self.id)
            .filter(doubles_code=self.doubles_code)
        )
        if others.count() > 1:
            raise ValidationError("Max two tanks per doubles code.")

    def get_absolute_url(self):
        return reverse("tank:detail", kwargs={"slug": self.code})

    def __str__(self):
        return smart_text(self.code)


class HydroManager(models.Manager):

    def __init__(self):
        super(HydroManager, self).__init__()

    def current(self, **kwargs):
        return self.filter(
            date__gte=date.today() - timedelta(days=1826),
            **kwargs
        )


class Hydro(TimeStampedModel):

    class Meta:
        ordering = ("date",)

    objects = HydroManager()

    tank = models.ForeignKey(Tank, null=False)
    date = models.DateField(null=False)


class VipManager(models.Manager):

    def __init__(self):
        super(VipManager, self).__init__()

    def current(self, **kwargs):
        return self.filter(
            date__gte=date.today() - timedelta(days=365),
            **kwargs
        )


class Vip(TimeStampedModel):

    class Meta:
        ordering = ("date",)

    objects = VipManager()

    tank = models.ForeignKey(Tank, null=False)
    date = models.DateField(null=False)

