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
                tank_code,
                gas_name,
                psi_start,
                psi_end,
                is_blend=False,
                is_equipment_surcharge=False,
                datetime=timezone.now()): # pylint: disable=too-many-locals,too-many-arguments
    '''create a Fill object from seven inputs plus an optional datetime'''

    user = User.objects.get(username=username)
    blender = Member.objects.get(user__username=blender)
    bill_to = Member.objects.get(user__username=bill_to)
    tank = Tank.objects.get(code=tank_code)
    cubic_feet = \
        (float(psi_end) - float(psi_start)) * tank.spec.tank_factor / 100.0

    equipment_price_proportional = 0.0
    total_price = cash(0.0)
    air_price = 0.0
    argon_price = 0.0
    helium_price = 0.0
    oxygen_price = 0.0
    other_price = 0.0
    gas_price = 0.0
    total_price = cash(0.0)

    if is_equipment_surcharge:
        equipment_price_fixed = float(settings.EQUIPMENT_COST_FIXED)
        equipment_price_proportional = cubic_feet * float(settings.EQUIPMENT_COST_PROPORTIONAL)
        total_price = cash(equipment_price_fixed + equipment_price_proportional)
        gas_name = "Equipment"
    else:
        gas = Gas.objects.get(name=gas_name)
        air_price = \
            cubic_feet * gas.air_fraction * float(settings.AIR_COST)
        argon_price = \
            cubic_feet * gas.argon_fraction * float(settings.ARGON_COST)
        helium_price = \
            cubic_feet * gas.helium_fraction * float(settings.HELIUM_COST)
        oxygen_price = \
            cubic_feet * gas.oxygen_fraction * float(settings.OXYGEN_COST)
        other_price = \
            cubic_feet * gas.other_fraction * float(settings.OTHER_COST)
        gas_price = \
            air_price + argon_price + helium_price + oxygen_price + other_price
        total_price = cash(gas_price)

    is_paid = bill_to.autopay_fills
    return Fill(
        datetime=datetime,
        user=user,
        blender=blender,
        bill_to=bill_to,
        tank_serial_number=tank.serial_number,
        tank_code=tank_code,
        tank_spec=tank.spec.name,
        tank_volume=tank.spec.volume,
        tank_working_pressure=tank.spec.working_pressure,
        tank_factor=tank.spec.tank_factor,
        gas_name=gas_name,
        gas_slug=slugify(gas_name),
        psi_start=psi_start,
        psi_end=psi_end,
        cubic_feet=cubic_feet,
        air_cost=settings.AIR_COST,
        argon_cost=settings.ARGON_COST,
        helium_cost=settings.HELIUM_COST,
        oxygen_cost=settings.OXYGEN_COST,
        other_cost=settings.OTHER_COST,
        air_price=air_price,
        argon_price=argon_price,
        helium_price=helium_price,
        oxygen_price=oxygen_price,
        other_price=other_price,
        gas_price=gas_price,
        equipment_price_proportional=equipment_price_proportional,
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
        if not self.blender.is_blender:
            raise ValidationError(
                "{0} is not a gas blender".format(self.blender.username)
            )
        if self.psi_start > self.psi_end:
            raise ValidationError("Psi Start must not exceed Psi_end")
        if self.is_equipment_surcharge:
            if self.gas_name or self.gas_slug:
                raise ValidationError("Equipment surcharges should not contain gas info")
            if (self.air_price or self.argon_price or hself.elium_price or oself.xygen_price or self.other_price):
                raise ValidationError("Gas prices should be zero for equipment surcharges")
        else:
            if not (self.gas_name and self.gas_slug):
                raise ValidationError("Gas fills should contain gas info")
            if self.equipment_price_proportional:
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
    # Log these in case someone changes the spec or price after the fact
    tank_serial_number = models.CharField(
        editable=False,
        max_length=30,
        verbose_name="Tank Serial Number"
    )
    tank_code = models.SlugField(
        max_length=30,
        verbose_name="Tank Code",
    )
    tank_spec = models.CharField(
        editable=False,
        max_length=30,
        verbose_name="Tank Spec",
    )
    tank_volume = models.FloatField(
        editable=False,
        default=0,
        verbose_name="Tank Volume",
    )
    tank_working_pressure = models.PositiveSmallIntegerField(
        editable=False,
        default=0,
        verbose_name="Tank Pressure",
    )
    tank_factor = models.FloatField(
        editable=False,
        default=0,
        verbose_name="Tank Factor",
    )

    gas_name = models.CharField(
        default="", #SDF
        editable=False,
        max_length=30,
        verbose_name="Gas"
    )
    gas_slug = models.SlugField(
        default="", #SDF
        null=False,
        editable=False,
    )

    psi_start = models.PositiveSmallIntegerField(
        default=0,
        editable=False,
        validators=[MinValueValidator(0), MaxValueValidator(4000)],
        verbose_name="Psi Start"
    )
    psi_end = models.PositiveSmallIntegerField(
        default=0,
        editable=False,
        validators=[MinValueValidator(0), MaxValueValidator(4000)],
        verbose_name="Psi End"
    )
    cubic_feet = models.FloatField(
        default=0.0,
        editable=False,
        verbose_name="Cubic Feet"
    )

    DEPRECATED_equipment_cost = models.DecimalField(
        decimal_places=2, max_digits=20,
        default=cash(0.0),
        editable=False,
        verbose_name="[DEPRECATED] Equipment Cost",
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
    other_cost = models.DecimalField(
        decimal_places=2, max_digits=20,
        default=settings.OTHER_COST,
        editable=False,
        verbose_name="Oxygen Cost",
    )
    equipment_cost_fixed = models.DecimalField(
        decimal_places=2, max_digits=20,
        default=cash(0.0), # TODO(stpyang): change this
        editable=False,
        verbose_name="Fixed Equipment Cost",
    )
    equipment_cost_proportional = models.DecimalField(
        decimal_places=2, max_digits=20,
        default=cash(0.0), # TODO(stpyang): change this
        editable=False,
        verbose_name="Proportional Equipment Cost",
    )

    DEPRECATED_equipment_price = models.FloatField(
        default=0.0,
        editable=False,
        verbose_name="[DEPRECATED] Equipment Price",
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
    other_price = models.FloatField(
        default=0.0,
        editable=False,
        verbose_name="Other Price"
    )
    gas_price = models.FloatField(
        default=0.0,
        editable=False,
        verbose_name="Gas Price"
    )
    equipment_price_proportional = models.FloatField(
        default=0.0,
        editable=False,
        verbose_name="Gas Price"
    )
    total_price = models.DecimalField(
        decimal_places=2,
        default=cash(0.0),
        editable=False,
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
        editable=False,
        help_text="Designates whether this is an equipment surcharge",
        verbose_name="Is Blend",
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
