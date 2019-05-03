'''Copyright 2016 DDNY. All Rights Reserved.'''

from calendar import monthrange
from datetime import date
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.encoding import smart_text
from django.utils.text import slugify
# from jsignature.mixins import JSignatureField
from model_utils.models import TimeStampedModel

from ddny_braintree.models import BraintreeTransactionMixin
from .validators import validate_user


class ZipCodeValidator(RegexValidator):
    '''Validates zip codes of the form xxxxx and xxxxx-xxxx'''

    regex = r"^\d{5}(-\d{4})?$"
    message = "Enter a valid postal code"


class MemberInfoMixin(models.Model):
    '''Member information for vip forms and stuff'''

    class Meta:
        abstract = True

    address = models.CharField(blank=True, max_length=30)
    city = models.CharField(blank=True, max_length=30)
    state = models.CharField(blank=True, max_length=2)
    zip_code = models.CharField(
        blank=True,
        max_length=10,
        validators=[ZipCodeValidator])
    phone_number = models.CharField(blank=True, max_length=12)
    psi_inspector_number = models.CharField(blank=True, max_length=30)
    blender_certification = models.CharField(blank=True, max_length=30)

    member_info_fields = (
        "address",
        "city",
        "state",
        "zip_code",
        "phone_number",
        "psi_inspector_number",
        "blender_certification",
    )


class MemberManager(models.Manager):

    def __init__(self):
        super(MemberManager, self).__init__()

    def is_blender(self, **kwargs):
        return self.filter(is_blender=True, **kwargs)


def add_months(startdate, months):
    '''helper function to calculate dues'''
    month = startdate.month - 1 + months
    year = int(startdate.year + month / 12)
    month = month % 12 + 1
    startdate = min(startdate.day, monthrange(year, month)[1])
    return date(year, month, startdate)


class Member(MemberInfoMixin, TimeStampedModel):
    '''club member'''

    def __str__(self):
        return smart_text(self.username)

    def get_absolute_url(self):
        return reverse("member_detail", kwargs={"slug": self.slug})

    def monthly_dues_current_until(self):
        paid_months = 0
        paid_months_query = MonthlyDues.objects.paid().filter(member=self)
        if paid_months_query:
            paid_months = paid_months_query.aggregate(models.Sum("months")).get("months__sum")
        return add_months(self.member_since, paid_months)

    @property
    def past_due(self):
        return self.monthly_dues_current_until() <= date.today()

    def save(self, **kwargs):
        if self.username:
            self.user.username = self.username
        else:
            self.username = self.user.username
        if self.first_name:
            self.user.first_name = self.first_name
        else:
            self.first_name = self.user.first_name
        if self.last_name:
            self.user.last_name = self.last_name
        else:
            self.last_name = self.user.last_name
        if self.email:
            self.user.email = self.email
        else:
            self.email = self.user.email
        self.user.save()
        self.slug = slugify(self.user.username)
        super(Member, self).save(kwargs)

    @property
    def current_consent(self):
        consents = ConsentA.objects.current().filter(member=self)
        if consents.count() > 0:
            return consents[0]

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    @property
    def initials(self):
        result = ""
        if self.first_name:
            result += self.first_name[0]
        if self.last_name:
            result += self.last_name[0]
        return result

    @property
    def last_consent(self):
        consents = ConsentA.objects \
            .filter(member=self)
        if consents:
            return consents[0]

    @property
    def last_login(self):
        return self.user.last_login # pragma: no cover

    class Meta:
        ordering = ("last_name", "first_name")

    objects = MemberManager()

    user = models.OneToOneField(
        User,
        null=False,
        validators=[validate_user],
        on_delete=models.CASCADE,
    )
    username = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(null=False, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    gender = models.CharField(
        max_length=6,
        choices=(
            ("female", "female"),
            ("male", "male"),
        ),
        default="male",
    )
    member_since = models.DateField(
        null=False,
    )
    is_blender = models.BooleanField(
        default=False,
        help_text="Designates whether the member is a certified gas blender"
    )
    autopay_fills = models.BooleanField(
        default=False,
        help_text="Raph only!"
    )
    is_treasurer = models.BooleanField(
        default=False,
        help_text="Designates whether the member can see additional fillstation accounting info"
    )
    honorary_member = models.BooleanField(
        default=False,
        help_text="Honorary members can view the website and have their tanks filled at the club"
    )

# class Certification(TimeStampedModel):
#     member = models.ForeignKey(Member)
#     STATUS = Choices(
#         "BSAC",
#         "CMAS",
#         "GUE",
#         "NACD",
#         "NAUI",
#         "PADI",
#         "SDI/TDI/ERDI",
#         "SSI",
#         "UTD",
#         ""
#     )
#     agency = StatusField(
#         default="",
#         db_index=True,
#         verbose_name="Certifying Agency",
#     )
#     level = models.CharField(max_length=30, null=False)
#     card_number = models.CharField(max_length=30, null=False)


# TODO(stpyang): make this a real abstract class
class AbstractConsent(TimeStampedModel):
    '''Abstract consent class which may be versioned'''

    def get_absolute_url(self):
        return reverse("consent_detail", kwargs={"pk": self.id})

    class Meta:
        abstract = True

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=30, null=False)
    # member_signature = JSignatureField(null=False)
    member_signature_date = models.DateField(null=False)
    witness_name = models.CharField(max_length=30, null=False)
    # witness_signature = JSignatureField(null=False)
    witness_signature_date = models.DateField(null=False)

    signature_fields = (
        "member_name",
        "member_signature",
        "member_signature_date",
        "witness_name",
        "witness_signature",
        "witness_signature_date",
    )

    signature_fields = (
        "member_name",
        "member_signature",
        "member_signature_date",
        "witness_name",
        "witness_signature",
        "witness_signature_date",
    )


class ConsentAManager(models.Manager):

    def __init__(self):
        super(ConsentAManager, self).__init__()

    def current(self, **kwargs):
        return self.filter(
            member_signature_date__gte=date.today() - relativedelta(years=1),
            **kwargs
        )


class ConsentA(AbstractConsent):
    '''consent version 1.0'''

    def __str__(self):
        return "{0} {1} v1.0".format(
            self.member_signature_date,
            self.member.full_name,
        )

    class Meta:
        ordering = ("-member_signature_date",)
        verbose_name = "Consent v1.0"
        verbose_name_plural = "Consents v1.0"

    objects = ConsentAManager()

    consent_is_experienced_certified_diver = models.BooleanField()
    consent_club_is_non_profit = models.BooleanField()
    consent_vip_tank = models.BooleanField()
    consent_examine_tank = models.BooleanField()
    consent_no_unsafe_tank = models.BooleanField()
    consent_analyze_gas = models.BooleanField()
    consent_compressed_gas_risk = models.BooleanField()
    consent_diving_risk = models.BooleanField()
    consent_sole_responsibility = models.BooleanField()
    consent_do_not_sue = models.BooleanField()
    consent_strenuous_activity_risk = models.BooleanField()
    consent_inspect_equipment = models.BooleanField()
    consent_lawful_age = models.BooleanField()
    consent_release_of_risk = models.BooleanField()

    boolean_fields = (
        "consent_is_experienced_certified_diver",
        "consent_club_is_non_profit",
        "consent_vip_tank",
        "consent_examine_tank",
        "consent_no_unsafe_tank",
        "consent_analyze_gas",
        "consent_compressed_gas_risk",
        "consent_diving_risk",
        "consent_sole_responsibility",
        "consent_do_not_sue",
        "consent_strenuous_activity_risk",
        "consent_inspect_equipment",
        "consent_lawful_age",
        "consent_release_of_risk",
    )


class MonthlyDuesManager(models.Manager):

    def __init__(self):
        super(MonthlyDuesManager, self).__init__()

    def paid(self, **kwargs):
        return self.filter(is_paid=True, **kwargs)

    def unpaid(self, **kwargs):
        return self.filter(is_paid=False, **kwargs)


class MonthlyDues(BraintreeTransactionMixin, TimeStampedModel):

    class Meta:
        verbose_name_plural = "Monthly Dues"

    objects = MonthlyDuesManager()

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    months = models.PositiveIntegerField()

    def __str__(self):
        if self.months == 1:
            return smart_text("{0} dues for {1} month".format(self.member.first_name, self.months))
        else:
            return smart_text("{0} dues for {1} months".format(self.member.first_name, self.months))
