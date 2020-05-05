'''Copyright 2016 DDNY. All Rights Reserved.'''

from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.encoding import smart_text
from django.utils.text import slugify

from model_utils.models import TimeStampedModel

from registration.models import Member


class Specification(TimeStampedModel):
    '''manufacturing specifications for tanks'''

    class Meta:
        '''https://docs.djangoproject.com/en/2.2/ref/models/options/#model-meta-options'''
        ordering = ("name",)

    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(null=False, blank=True, unique=True)
    material = models.CharField(
        max_length=8,
        choices=(
            ("Aluminum", "Aluminum"),
            ("Steel", "Steel"),
            ("FRP", "FRP"),
            ("Composite", "Composite"),
        ),
        default='Aluminum',
    )
    volume = models.FloatField()  # cubic feet only
    working_pressure = models.PositiveSmallIntegerField()  # psi only

    @property
    def tank_factor(self):
        return 100.0 * self.volume / self.working_pressure

    def get_absolute_url(self):
        return reverse("spec_detail", kwargs={"slug": self.slug})

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
        ordering = ("owner__first_name", "code",)

    def __str__(self):
        return smart_text(self.code)

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

    @property
    def first_hydro(self):
        result = Hydro.objects.filter(tank=self).reverse()
        if result:
            return result[0]

    @property
    def is_current_hydro(self):
        return Hydro.objects.current().filter(tank=self).count() > 0

    @property
    def is_current_vip(self):
        return Vip.objects.current().filter(tank=self).count() > 0

    @property
    def last_hydro(self):
        result = Hydro.objects.filter(tank=self)
        if result:
            return result[0]

    @property
    def last_vip(self):
        result = Vip.objects.filter(tank=self)
        if result:
            return result[0]

    @property
    def tank_factor(self):
        return self.spec.tank_factor


    objects = TankManager()

    serial_number = models.SlugField(null=False, unique=True)
    owner = models.ForeignKey(Member, null=False, on_delete=models.CASCADE)
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
    spec = models.ForeignKey(Specification, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this tank should be treated as active. \
            Unselect this instead of deleting tanks.",
        verbose_name="Active",
    )


class HydroManager(models.Manager):

    def __init__(self):
        super(HydroManager, self).__init__()

    def current(self, **kwargs):
        return self.filter(
            date__gte=date.today() - relativedelta(years=5),
            **kwargs
        )


class Hydro(TimeStampedModel):
    '''Hydrostatic testing'''
    def __str__(self):
        return smart_text(self.date.strftime("%Y-%m-%d"))

    class Meta:
        ordering = ("-date",)

    objects = HydroManager()

    tank = models.ForeignKey(Tank, null=False, on_delete=models.CASCADE)
    date = models.DateField(null=False)


class VipManager(models.Manager):

    def __init__(self):
        super(VipManager, self).__init__()

    def current(self, **kwargs):
        return self.filter(
            date__gte=date.today() - relativedelta(years=1),
            **kwargs
        )


class Vip(TimeStampedModel):
    '''Digital representation of psi/pci vip form'''

    def __str__(self):
        return smart_text(self.date.strftime("%Y-%m-%d"))

    def get_absolute_url(self):
        return reverse("vip_detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ("-date",)

    objects = VipManager()

    tank = models.ForeignKey(Tank, null=False, on_delete=models.CASCADE)
    tank_owners_name = models.CharField(blank=True, max_length=30)
    date = models.DateField(null=False)
    address = models.CharField(blank=True, max_length=30)
    city = models.CharField(blank=True, max_length=30)
    state = models.CharField(blank=True, max_length=2)
    zip_code = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(blank=True, max_length=30)
    tank_spec_name = models.CharField(blank=True, max_length=30)
    tank_serial_number = models.SlugField(blank=True)
    tank_first_hydro_date = models.DateField(null=True)
    tank_last_hydro_date = models.DateField(null=True)
    tank_specification = models.CharField(blank=True, max_length=30)
    tank_working_pressure = models.PositiveSmallIntegerField(
        blank=True,
        null=True)  # psi only
    tank_material = models.CharField(
        max_length=8,
        choices=(
            ('Aluminum', 'Aluminum'),
            ('Steel', 'Steel'),
            ('FRP', 'FRP'),
            ('Composite', 'Composite'),
        ),
        default='Aluminum',
    )

    # EXTERNAL
    # external_evidence_of_heat_damage = models.BooleanField(default=False)
    external_evidence_of_heat_damage = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    external_repainting = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    external_odor = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    external_bow = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    external_evidence_of_bulges = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    external_hammer_tone_test = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    external_description_of_surface = models.CharField(blank=True, max_length=255)
    external_line_corrosion = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    external_comparison_to_psi_standards = models.CharField(
        max_length=8,
        choices=(
            ("Accept", "Accept"),
            ("Reject", "Reject"),
            ("Condemn", "Condemn"),
        ),
        default="Accept",
    )

    # INTERNAL
    internal_composition_of_contents = models.CharField(blank=True, max_length=255,)
    internal_description_of_surface = models.CharField(blank=True, max_length=255)
    internal_pitting = models.CharField(blank=True, max_length=255)
    internal_comparison_to_psi_standards = models.CharField(
        max_length=8,
        choices=(
            ("Accept", "Accept"),
            ("Reject", "Reject"),
            ("Condemn", "Condemn"),
        ),
        default="Accept",
    )

    # THREADS
    threads_description = models.CharField(blank=True, max_length=255)
    threads_crack_assessment = models.CharField(blank=True, max_length=255)
    threads_oring_gland_surface = models.CharField(blank=True, max_length=255)
    threads_eddy_current_test = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    threads_comparison_to_psi_standards = models.CharField(
        max_length=8,
        choices=(
            ("Accept", "Accept"),
            ("Reject", "Reject"),
            ("Condemn", "Condemn"),
        ),
        default="Accept",
    )

    # VALVE
    valve_service_needed = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    valve_burst_disc_replaced = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    valve_oring_replaced = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    valve_dip_tube_replaced = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    valve_threads_checked = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="No",
    )
    valve_thread_condition = models.CharField(blank=True, max_length=255)

    # CYLINDER CONDITION
    cylindercondition = models.CharField(
        max_length=8,
        choices=(
            ("Accept", "Accept"),
            ("Reject", "Reject"),
            ("Condemn", "Condemn"),
        ),
        default="Accept",
    )
    cylindercondition_sticker_affixed = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No"),),
        default="Yes",
    )
    cylindercondition_sticker_notation = models.CharField(blank=True, max_length=255)
    cylindercondition_sticker_date = models.DateField(null=True)
    cylindercondition_clean = models.BooleanField(default=False)
    cylindercondition_tumble = models.BooleanField(default=False)
    cylindercondition_hydro = models.BooleanField(default=False)
    cylindercondition_other = models.BooleanField(default=False)
    cylindercondition_inspector_initials = models.CharField(blank=True, max_length=5)
    cylindercondition_discard = models.BooleanField(default=False)
    inspector_name = models.CharField(null=False, max_length=50)
    inspector_psi_number = models.CharField(blank=True, max_length=30)

    header_fields = (
        "tank",
        "tank_owners_name",
        "date",
        "address",
        "city",
        "state",
        "zip_code",
        "phone_number",
    )

    tank_fields = (
        "tank_spec_name",
        "tank_serial_number",
        "tank_first_hydro_date",
        "tank_last_hydro_date",
        "tank_specification",
        "tank_working_pressure",
        "tank_material",
    )

    external_fields = (
        "external_evidence_of_heat_damage",
        "external_repainting",
        "external_odor",
        "external_bow",
        "external_evidence_of_bulges",
        "external_hammer_tone_test",
        "external_description_of_surface",
        "external_line_corrosion",
        "external_comparison_to_psi_standards",
    )

    internal_fields = (
        "internal_composition_of_contents",
        "internal_description_of_surface",
        "internal_pitting",
        "internal_comparison_to_psi_standards",
    )

    threads_fields = (
        "threads_description",
        "threads_crack_assessment",
        "threads_oring_gland_surface",
        "threads_eddy_current_test",
        "threads_comparison_to_psi_standards",
    )

    valve_fields = (
        "valve_service_needed",
        "valve_burst_disc_replaced",
        "valve_oring_replaced",
        "valve_dip_tube_replaced",
        "valve_threads_checked",
        "valve_thread_condition",
    )

    cylindercondition_fields = (
        "cylindercondition",
        "cylindercondition_sticker_affixed",
        "cylindercondition_sticker_date",
        "cylindercondition_sticker_notation",
        "cylindercondition_clean",
        "cylindercondition_tumble",
        "cylindercondition_hydro",
        "cylindercondition_other",
        "cylindercondition_inspector_initials",
        "cylindercondition_discard",
    )

    inspector_fields = (
        "inspector_name",
        "inspector_psi_number",
    )
