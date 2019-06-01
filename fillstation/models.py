'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.text import slugify

from model_utils.models import TimeStampedModel

from ddny_braintree.models import BraintreeTransactionMixin
from ddny.core import cash
from registration.models import Member
from tank.models import Tank
from gas.models import Gas


def _build_fill(username,
                blender,
                bill_to,
                equipment_surcharge_key=None,
                tank_code=None,
                gas_name=None,
                psi_start=None,
                psi_end=None,
                is_blend=False,
                is_equipment_surcharge=False,
                datetime=timezone.now()): # pylint: disable=too-many-locals,too-many-arguments
    '''create a Fill object from seven inputs plus an optional datetime'''

    user = User.objects.get(username=username)
    blender = Member.objects.get(user__username=blender)
    bill_to = Member.objects.get(user__username=bill_to)
    tank_serial_number = None
    tank_name = None
    tank_volume = None
    tank_working_pressure = None
    tank_factor = None
    cubic_feet = None

    air_price = 0.0
    argon_price = 0.0
    helium_price = 0.0
    oxygen_price = 0.0
    equipment_price = 0.0
    total_price = settings.EQUIPMENT_COST_FIXED

    if not is_equipment_surcharge:
        tank = Tank.objects.get(code=tank_code)
        tank_serial_number = tank.serial_number
        tank_name = tank.spec.name
        tank_volume = tank.spec.volume
        tank_working_pressure = tank.spec.working_pressure
        tank_factor = tank.spec.tank_factor

        cubic_feet = (float(psi_end) - float(psi_start)) * tank_factor / 100.0

        gas = Gas.objects.get(name=gas_name)
        air_price = \
            cubic_feet * gas.air_fraction * float(settings.AIR_COST)
        argon_price = \
            cubic_feet * gas.argon_fraction * float(settings.ARGON_COST)
        helium_price = \
            cubic_feet * gas.helium_fraction * float(settings.HELIUM_COST)
        oxygen_price = \
            cubic_feet * gas.oxygen_fraction * float(settings.OXYGEN_COST)
        equipment_price = \
            cubic_feet * float(settings.EQUIPMENT_COST_PROPORTIONAL)
        total_price = cash(
            air_price + argon_price + helium_price + oxygen_price + equipment_price
        )

    is_paid = bill_to.autopay_fills
    return Fill(
        datetime=datetime,
        user=user,
        blender=blender,
        bill_to=bill_to,
        equipment_surcharge_key=equipment_surcharge_key,
        tank_serial_number=tank_serial_number,
        tank_code=tank_code,
        tank_spec=tank_name,
        tank_volume=tank_volume,
        tank_working_pressure=tank_working_pressure,
        tank_factor=tank_factor,
        gas_name=gas_name,
        gas_slug=slugify(gas_name),
        psi_start=psi_start,
        psi_end=psi_end,
        cubic_feet=cubic_feet,
        air_cost=settings.AIR_COST,
        argon_cost=settings.ARGON_COST,
        helium_cost=settings.HELIUM_COST,
        oxygen_cost=settings.OXYGEN_COST,
        equipment_cost_proportional=settings.EQUIPMENT_COST_PROPORTIONAL,
        equipment_cost_fixed=settings.EQUIPMENT_COST_FIXED,
        air_price=air_price,
        argon_price=argon_price,
        helium_price=helium_price,
        oxygen_price=oxygen_price,
        equipment_price_proportional=equipment_price,
        total_price=total_price,
        is_blend=is_blend,
        is_equipment_surcharge=is_equipment_surcharge,
        is_paid=is_paid,
    )


class FillManager(models.Manager):

    def paid(self, **kwargs):
        return self.filter(is_paid=True, **kwargs)

    def unpaid(self, **kwargs):
        return self.filter(is_paid=False, **kwargs)


class Fill(BraintreeTransactionMixin, TimeStampedModel): # pylint: disable=too-many-locals
    '''
        This is the obejct which represents one line in the fillstation log.
        Try to avoid using any ForeignKey fields since this creates dependencies
        in the database which make the log less robust.  For example, setting
        tank = ForeignKey(Tank) would mean that the log could be retroactively
        changed by editing the associated Tank object.  Even worse, Fill objects
        would be deleted if a Tank were deleted.
    '''

    def __str__(self):
        return smart_text("{0} {1} {2}".format(
            self.id,
            str(self.datetime),
            self.blender
        ))

    def clean(self):
        super(Fill, self).clean()
        contains_gas_info = (self.gas_name and self.gas_slug and self.gas_slug != slugify(None))
        if not self.blender.is_blender:
            raise ValidationError(
                "{0} is not a gas blender".format(self.blender.username)
            )
        if (self.psi_start is not None and self.psi_end is not None and
                (self.psi_start > self.psi_end)):
            raise ValidationError("Psi Start must not exceed Psi_end")
        if self.is_equipment_surcharge:
            if contains_gas_info:
                raise ValidationError("Equipment surcharges should not contain gas info")
            if (self.air_price or self.argon_price or self.helium_price or self.oxygen_price):
                raise ValidationError("Gas prices should be zero for equipment surcharges")
        else:
            if not contains_gas_info:
                raise ValidationError("Gas fills should contain gas info")
            if not self.equipment_price_proportional:
                raise ValidationError("Proportional equipment price should be zero for gas fills")


    class Meta:
        ordering = ("-datetime", "-id",)

    objects = FillManager()

    datetime = models.DateTimeField(
        default=timezone.now,
        verbose_name="Time"
    )
    # this is the account which created the fill, i.e. can be a dummy account
    user = models.ForeignKey(
        User,
        verbose_name="User",
        related_name="%(app_label)s_%(class)s_owner_related",
        on_delete=models.CASCADE,
    )
    # this is the club member who filled the tanks, must be a person
    blender = models.ForeignKey(
        Member,
        verbose_name="Blender",
        related_name="%(app_label)s_%(class)s_blender_related",
        on_delete=models.CASCADE,
    )
    # this is the club member who will pay for fills, must be a person
    bill_to = models.ForeignKey(
        Member,
        verbose_name="Bill To",
        related_name="%(app_label)s_%(class)s_bill_to_related",
        on_delete=models.CASCADE,
    )
    equipment_surcharge_key = models.CharField(
        blank=True,
        default=None,
        max_length=30,
        verbose_name="Equipment Surcharge Key",
        null=True,
    )
    # Log these in case someone changes the spec or price after the fact
    tank_serial_number = models.CharField(
        editable=False,
        max_length=30,
        verbose_name="Tank Serial Number",
        null=True,
    )
    tank_code = models.SlugField(
        blank=True,
        default=None,
        max_length=30,
        verbose_name="Tank Code",
        null=True,
    )
    tank_spec = models.CharField(
        editable=False,
        max_length=30,
        verbose_name="Tank Spec",
        null=True,
    )
    tank_volume = models.FloatField(
        editable=False,
        verbose_name="Tank Volume",
        null=True,
    )
    tank_working_pressure = models.PositiveSmallIntegerField(
        editable=False,
        verbose_name="Tank Pressure",
        null=True,
    )
    tank_factor = models.FloatField(
        editable=False,
        verbose_name="Tank Factor",
        null=True,
    )

    gas_name = models.CharField(
        default="", #SDF
        editable=False,
        max_length=30,
        verbose_name="Gas",
        null=True,
    )
    gas_slug = models.SlugField(
        default="", #SDF
        editable=False,
        null=True,
    )

    psi_start = models.PositiveSmallIntegerField(
        editable=False,
        validators=[MinValueValidator(0), MaxValueValidator(4000)],
        verbose_name="Psi Start",
        null=True,
    )
    psi_end = models.PositiveSmallIntegerField(
        editable=False,
        validators=[MinValueValidator(0), MaxValueValidator(4000)],
        verbose_name="Psi End",
        null=True,
    )
    cubic_feet = models.FloatField(
        editable=False,
        verbose_name="Cubic Feet",
        null=True,
    )

    air_cost = models.DecimalField(
        decimal_places=2, max_digits=20,
        editable=False,
        default=settings.AIR_COST,
        verbose_name="Air Cost",
    )
    argon_cost = models.DecimalField(
        decimal_places=2, max_digits=20,
        editable=False,
        default=settings.ARGON_COST,
        verbose_name="Argon Cost",
    )
    helium_cost = models.DecimalField(
        decimal_places=2, max_digits=20,
        default=settings.HELIUM_COST,
        editable=False,
        verbose_name="Helium Cost",
    )
    oxygen_cost = models.DecimalField(
        decimal_places=2, max_digits=20,
        default=settings.OXYGEN_COST,
        editable=False,
        verbose_name="Oxygen Cost",
    )
    equipment_cost_fixed = models.DecimalField(
        decimal_places=2, max_digits=20,
        default=settings.EQUIPMENT_COST_FIXED, # TODO(stpyang): change this
        editable=False,
        verbose_name="Fixed Equipment Cost",
    )
    equipment_cost_proportional = models.DecimalField(
        decimal_places=2, max_digits=20,
        default=settings.EQUIPMENT_COST_PROPORTIONAL, # TODO(stpyang): change this
        editable=False,
        verbose_name="Proportional Equipment Cost",
    )

    air_price = models.FloatField(
        default=0.0,
        editable=False,
        verbose_name="Air Price"
    )
    argon_price = models.FloatField(
        default=0.0,
        editable=False,
        verbose_name="Argon Price"
    )
    helium_price = models.FloatField(
        default=0.0,
        editable=False,
        verbose_name="Helium Price"
    )
    oxygen_price = models.FloatField(
        default=0.0,
        editable=False,
        verbose_name="Oxygen Price"
    )
    equipment_price_proportional = models.FloatField(
        default=0.0,
        editable=False,
        verbose_name="Equipment Price"
    )
    total_price = models.DecimalField(
        decimal_places=2,
        default=cash(0.0),
        max_digits=20,
        verbose_name="Total Price (for gas or equipment)")
    is_blend = models.BooleanField(
        default=False,
        editable=False,
        help_text="Designates whether this fill was part of a partial pressure blend",
        verbose_name="Is Blend",
    )
    is_equipment_surcharge = models.BooleanField(
        default=False,
        help_text="Designates whether this is an equipment surcharge",
        verbose_name="Is Equipment Surcharge",
    )


class PrepayManager(models.Manager):

    def paid(self, **kwargs):
        return self.filter(is_paid=True, **kwargs)

    def unpaid(self, **kwargs):
        return self.filter(is_paid=False, **kwargs)


class Prepay(BraintreeTransactionMixin, TimeStampedModel):
    '''A model which keeps track of both prepaid deposits amounts, as well
       as the fills that the prepaid balance are applied to'''
    class Meta:
        verbose_name_plural = "Prepay"

    objects = PrepayManager()

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        verbose_name="Amount",
    )
    fill = models.ForeignKey(
        Fill,
        blank=True,
        default=None,
        null=True,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return smart_text("{0} paid {1}".format(self.member.first_name, self.amount))
