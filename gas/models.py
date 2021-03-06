'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.encoding import smart_text
from django.utils.text import slugify

from model_utils.models import TimeStampedModel

from ddny.core import cash
from ddny.settings import costs


class Gas(TimeStampedModel):
    '''Specify the fraction of the gas in terms of its base compoments.'''

    class Meta:
        '''https://docs.djangoproject.com/en/2.2/ref/models/options/#model-meta-options'''

        verbose_name_plural = 'Gases'
        ordering = ('name',)

    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(null=False, unique=True)

    # NOTE(stpyang): validation is done in html5 and not python
    # There is no point in setting min_ and max_values here
    argon_percentage = models.DecimalField(
        decimal_places=1,
        default=cash(0),
        max_digits=5,
        verbose_name='Percentage Argon',
    )

    helium_percentage = models.DecimalField(
        decimal_places=1,
        default=cash(0),
        max_digits=5,
        verbose_name='Percentage Helium',
    )

    # this is the total percentage of oxygen in the air
    # e.g. Nitrox 32 => 32
    # e.g. Trimix 18/45 => 18
    oxygen_percentage = models.DecimalField(
        decimal_places=1,
        default=cash(0),
        max_digits=5,
        verbose_name='Percentage Oxygen',
    )

    other_percentage = models.DecimalField(
        decimal_places=1,
        default=cash(0),
        max_digits=5,
        verbose_name='Percentage Other',
    )

    is_banked = models.BooleanField(
        default=False,
        help_text='Designates whether this gas is banked.',
        verbose_name='Is Banked',
    )

    # NOTE(stpyang):
    #  20.9 * air_fraction + 100.0 * oxygen_fraction = oxygen_%
    # 100.0 * air_fraction + 100.0 * oxygen_fraction = 100 - argon_% - helium_%

    @property
    def air_fraction(self):
        '''returns the proportion (between 0 and 1) of the gas which is air'''
        return (100 - float(self.argon_percentage) - float(self.helium_percentage) -
                float(self.oxygen_percentage) - float(self.other_percentage)) / (100.0 - 20.9)

    @property
    def argon_fraction(self):
        '''returns the proportion (between 0 and 1) of the gas which is argon'''
        return float(self.argon_percentage) / 100.0

    @property
    def helium_fraction(self):
        '''returns the proportion (between 0 and 1) of the gas which is helium'''
        return float(self.helium_percentage) / 100.0

    # this is the amount of oxygen we have to fill from the banks
    # e.g. Nitrox 32 => 0.14
    # e.g. Trimix 18/45 => almost zero
    @property
    def oxygen_fraction(self):
        '''returns the proportion (between 0 and 1) of the gas which is oxygen'''
        return (.209 * float(self.argon_percentage) +
                .209 * float(self.helium_percentage) +
                float(self.oxygen_percentage) +
                .209 * float(self.other_percentage) - 20.9) / (100 - 20.9)

    @property
    def other_fraction(self):
        '''returns the proportion (between 0 and 1) of the gas which is other'''
        return float(self.other_percentage) / 100.0

    @property
    def cost(self):
        '''automatically compute the total cost of the gas'''
        return (
            self.air_fraction * float(costs.AIR_COST) +
            self.argon_fraction * float(costs.ARGON_COST) +
            self.helium_fraction * float(costs.HELIUM_COST) +
            self.oxygen_fraction * float(costs.OXYGEN_COST)
        )

    def clean(self):
        super(Gas, self).clean()
        if self.argon_percentage + self.helium_percentage \
                + self.oxygen_percentage + self.other_percentage > 100:
            raise ValidationError(
                'Total percentage of argon + helium + oxygen + other cannot exceed 100'
            )

    def get_absolute_url(self):  # pylint: disable=no-self-use
        '''https://docs.djangoproject.com/en/2.2/ref/models/instances/#get-absolute-url'''

        return reverse('gas:detail', kwargs={'slug': self.slug})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        '''https://docs.djangoproject.com/en/2.2/ref/models/instances/#saving-objects'''

        self.slug = slugify(self.name)
        super(Gas, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return smart_text(self.name)
