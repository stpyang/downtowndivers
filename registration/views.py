'''Copyright 2015 DDNY New York. All Rights Reserved.'''

from base64 import b64encode
from braces.views import LoginRequiredMixin
from io import BytesIO

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from jsignature.utils import draw_signature
import django.contrib.auth.views as auth_views

from ddny.decorators import consent_required
from ddny.mixins import ConsentRequiredMixin, WarnIfSuperuserMixin
from ddny.views import AbstractActionMixin
from .models import ConsentA, Member


class MemberActionMixin(AbstractActionMixin):
    '''set a message of a member is edited'''
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )


class MemberDetail(LoginRequiredMixin,
                   ConsentRequiredMixin,
                   WarnIfSuperuserMixin,
                   DetailView):
    model = Member
    context_object_name = "member"
    slug_field = "slug"


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


class ConsentACreate(LoginRequiredMixin, CreateView):
    '''
    Create a consent form v1.0

    Since an unauthenticaed user has no attribute "member", this view raises
    a 404 error instead of redirecting to login
    '''
    model = ConsentA

    fields = (
        "member",
        "member_name",
        "member_signature",
        "member_signature_date",
        "witness_name",
        "witness_signature",
        "witness_signature_date",
    ) + ConsentA.boolean_fields

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and not hasattr(request.user, "member"):
            raise Http404
        return super(ConsentACreate, self).dispatch(
            request, *args, **kwargs)


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
