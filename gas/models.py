'''Copyright 2016 DDNY. All Rights Reserved.'''

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import smart_text
from django.utils.text import slugify

from model_utils.models import TimeStampedModel


class GasManager(models.Manager):

    def __init__(self):
        super(GasManager, self).__init__()

    def is_banked(self, **kwargs):
        return self.filter(is_banked=True, **kwargs)


class Gas(TimeStampedModel):
    '''Specify the fraction of the gas in terms of its base compoments.'''

    class Meta:
        verbose_name_plural = "Gases"
        ordering = ("name",)

    objects = GasManager()

    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(null=False, unique=True)

    # NOTE(stpyang): validation is done in html5 and not python
    # There is no point in setting min_ and max_values here
    argon_percentage = models.DecimalField(
        decimal_places=1,
        default=Decimal(0.0),
        max_digits=5,
        verbose_name='Percentage Argon',
    )

    helium_percentage = models.DecimalField(
        decimal_places=1,
        default=Decimal(0.0),
        max_digits=5,
        verbose_name='Percentage Helium',
    )

    # this is the total percentage of oxygen in the air
    # e.g. Nitrox 32 => 32
    # e.g. Trimix 18/45 => 18
    oxygen_percentage = models.DecimalField(
        decimal_places=1,
        default=Decimal(0.0),
        max_digits=5,
        verbose_name='Percentage Oxygen',
    )

    is_banked = models.BooleanField(
        default=False,
        help_text="Designates whether this gas is banked.",
        verbose_name="Is Banked",
    )

    # NOTE(stpyag):
    #  20.9 * air_fraction + 100.0 * oxygen_fraction = oxygen_%
    # 100.0 * air_fraction + 100.0 * oxygen_fraction = 100 - argon_% - helium_%

    @property
    def air_fraction(self):
        return (100 - float(self.argon_percentage) - float(self.helium_percentage) - \
            float(self.oxygen_percentage)) / (100.0 - 20.9)

    @property
    def argon_fraction(self):
        return float(self.argon_percentage) / 100.0

    @property
    def helium_fraction(self):
        return float(self.helium_percentage) / 100.0

    # this is the amount of oxygen we have to fill from the banks
    # e.g. Nitrox 32 => 0.14
    # e.g. Trimix 18/45 => almost zero
    @property
    def oxygen_fraction(self):
        return (.209 * float(self.argon_percentage) + \
            .209 * float(self.helium_percentage) + \
            float(self.oxygen_percentage) - 20.9) / (100 - 20.9)

    @property
    def cost(self):
        return (
            self.air_fraction * float(settings.AIR_COST) + \
            self.argon_fraction * float(settings.ARGON_COST) + \
            self.helium_fraction * float(settings.HELIUM_COST) + \
            self.oxygen_fraction * float(settings.OXYGEN_COST)
        )

    def clean(self):
        super(Gas, self).clean()
        if self.argon_percentage + self.helium_percentage \
            + self.oxygen_percentage > 100:
            raise ValidationError(
                "Total percentage of argon + helium + and oxygen cannot exceed 100"
            )

    def get_absolute_url(self):
        return reverse("gas:detail", kwargs={"slug": self.slug})

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(Gas, self).save(kwargs)

    def __str__(self):
        return smart_text(self.name)
