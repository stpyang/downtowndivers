'''Copyright 2015 DDNY New York. All Rights Reserved.'''

from base64 import b64encode
from braces.views import LoginRequiredMixin
from io import BytesIO

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from jsignature.utils import draw_signature
import django.contrib.auth.views as auth_views

from .models import ConsentA, Member
from ddny.decorators import consent_required
from ddny.mixins import ConsentRequiredMixin, WarnIfSuperuserMixin
from ddny.views import AbstractActionMixin
from tank.models import Tank


class MemberActionMixin(AbstractActionMixin):
    '''set a message of a member is edited'''
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "gender",
        "address",
        "city",
        "state",
        "zip_code",
        "phone_number",
        "psi_inspector_number",
        "blender_certification_number",
    )


class MemberDetail(LoginRequiredMixin,
                   ConsentRequiredMixin,
                   WarnIfSuperuserMixin,
                   DetailView):
    model = Member
    context_object_name = "member"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(MemberDetail, self).get_context_data(**kwargs)
        context["tank_list"] = Tank.objects.filter(owner=self.object)
        return context


class MemberList(LoginRequiredMixin,
                 ConsentRequiredMixin,
                 WarnIfSuperuserMixin,
                 ListView):
    model = Member
    context_object_name = "member_list"


class MemberUpdate(LoginRequiredMixin,
                   ConsentRequiredMixin,
                   WarnIfSuperuserMixin,
                   MemberActionMixin,
                   UpdateView):
    model = Member
    context_object_name = "member"
    slug_field = "slug"

    def success_msg(self):
        return "The member \"{0}\" was updated successfully.".format(self.object)

    def get_object(self, *args, **kwargs):
        __object = super(MemberUpdate, self).get_object(*args, **kwargs)
        if self.request.user == __object.user or self.request.user.is_superuser:
            return __object
        else:
            raise PermissionDenied


class ConsentAActionMixin(AbstractActionMixin):
    '''set a message when the consent for is signed'''
    fields = ("member",) + ConsentA.signature_fields + ConsentA.boolean_fields


class ConsentACreate(LoginRequiredMixin, ConsentAActionMixin, CreateView):
    '''Create a consent form v1.0'''
    model = ConsentA

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and not hasattr(request.user, "member"):
            raise Http404
        return super(ConsentACreate, self).dispatch(
            request, *args, **kwargs)

    def success_msg(self):
        return "Thank you for signing the DDNY consent form!"


class ConsentADetail(LoginRequiredMixin,
                     ConsentRequiredMixin,
                     WarnIfSuperuserMixin,
                     DetailView):
    model = ConsentA
    context_object_name = "consent"
    slug_field = "id"

    def get_context_data(self, **kwargs):
        context = super(ConsentADetail, self).get_context_data(**kwargs)

        member_output = BytesIO()
        member_signature_image = draw_signature(self.object.member_signature)
        member_signature_image.save(member_output, format="PNG")
        member_signature_image_data = b64encode(member_output.getvalue())
        member_output.close()
        context["member_signature_image_data"] = member_signature_image_data

        witness_output = BytesIO()
        witness_signature_image = draw_signature(self.object.witness_signature)
        witness_signature_image.save(witness_output, format="PNG")
        witness_signature_image_data = b64encode(witness_output.getvalue())
        witness_output.close()
        context["witness_signature_image_data"] = witness_signature_image_data

        return context


def login(request, *args, **kwargs):
    if not request.method == "POST":
        if not request.POST.get("remember_me", None):
            request.session.set_expiry(0)
    return auth_views.login(request, *args, **kwargs)


@consent_required
def password_change(request, *args, **kwargs):
    return auth_views.password_change(request, *args, **kwargs)


@consent_required
def password_change_done(request, *args, **kwargs):
    return auth_views.password_change_done(request, *args, **kwargs)
