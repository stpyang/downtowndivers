'''Copyright 2016 DDNY New York. All Rights Reserved.'''

from base64 import b64encode
from io import BytesIO
import braintree

from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import django.contrib.auth.views as auth_views
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from jsignature.utils import draw_signature

from ddny.decorators import warn_if_superuser
from ddny.mixins import ConsentRequiredMixin, WarnIfSuperuserMixin
from ddny.settings import costs
from ddny.views import AbstractActionMixin
from fillstation.models import Fill
from tank.models import Tank
from .models import ConsentA, Member


@warn_if_superuser
@login_required
def pay_dues(request, **kwargs):
    '''members pay their dues by month'''
    if braintree.Configuration.environment == braintree.Environment.Sandbox:
        messages.warning(
            request, 'Payments are connected to braintree sandbox!'
        )
    if not request.user.member.slug == kwargs.get('slug'):
        raise PermissionDenied
    context = {
        'braintree_client_token': settings.BRAINTREE_CLIENT_TOKEN,
        'monthly_dues': costs.MONTHLY_DUES,
    }
    return render(request, 'registration/pay_dues.html', context)


class MemberActionMixin(AbstractActionMixin):
    '''set a message of a member is edited'''

    @property
    def success_msg(self):
        return super(MemberActionMixin).success_msg

    @property
    def cancel_msg(self):
        return super(MemberActionMixin).cancel_msg

    @property
    def cancel_url(self):
        return super(MemberActionMixin).cancel_url

    fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'gender',
        'psi_inspector_number',
        'blender_certification',
    ) + Member.address_fields


class MemberDetail(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, DetailView):
    '''https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#detailview'''

    model = Member
    context_object_name = 'member'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(MemberDetail, self).get_context_data(**kwargs)
        context['fill_list'] = Fill.objects.filter(bill_to=self.object)[:10]
        context['tank_list'] = Tank.objects.filter(owner=self.object).filter(is_active=True)
        return context


class MemberList(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, ListView):
    '''https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#listview'''

    model = Member
    context_object_name = 'member_list'

    def get_context_data(self, **kwargs):
        context = super(MemberList, self).get_context_data(**kwargs)
        member_emails = map(
            lambda member: member.email,
            Member.objects.filter(honorary_member=False)
        )
        context['member_emails'] = ','.join(list(member_emails))
        return context

    def get_queryset(self):
        return Member.objects.filter(honorary_member=False)


class MemberUpdate(LoginRequiredMixin, WarnIfSuperuserMixin, MemberActionMixin, UpdateView):
    '''update member info'''
    model = Member
    context_object_name = 'member'
    slug_field = 'slug'

    @property
    def success_msg(self):
        return 'The member \'{0}\' was updated successfully!'.format(self.object)

    @property
    def cancel_msg(self):
        return 'The member \'{0}\' was not updated!'.format(self.get_object())

    @property
    def cancel_url(self):
        return self.get_object().get_absolute_url()

    def get_object(self, queryset=None):
        __object = super(MemberUpdate, self).get_object(queryset)
        if self.request.user == __object.user:
            return __object
        raise Http404


class ConsentACreate(LoginRequiredMixin, WarnIfSuperuserMixin, CreateView):
    '''Create a consent form v1.1'''
    model = ConsentA

    fields = [field.name for field in ConsentA._meta.get_fields() if field.editable]

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not hasattr(request.user, 'member'):
            raise Http404
        return super(ConsentACreate, self).dispatch(
            request, *args, **kwargs)

    @property
    def success_msg(self):
        '''be polite'''
        return 'Thank you for signing the DDNY consent form!'


class ConsentADetail(LoginRequiredMixin, ConsentRequiredMixin, WarnIfSuperuserMixin, DetailView):
    '''https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#detailview'''

    model = ConsentA
    context_object_name = 'consent'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super(ConsentADetail, self).get_context_data(**kwargs)

        member_output = BytesIO()
        member_signature_image = draw_signature(self.object.member_signature)
        member_signature_image.save(member_output, format='PNG')
        member_signature_image_data = b64encode(member_output.getvalue()).decode('utf-8')
        member_output.close()
        context['member_signature_image_data'] = member_signature_image_data

        witness_output = BytesIO()
        witness_signature_image = draw_signature(self.object.witness_signature)
        witness_signature_image.save(witness_output, format='PNG')
        witness_signature_image_data = b64encode(witness_output.getvalue()).decode('utf-8')
        witness_output.close()
        context['witness_signature_image_data'] = witness_signature_image_data

        return context


def login(request, *args, **kwargs):
    '''self-explanatory'''
    if not request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return auth_views.LoginView.as_view()(request, *args, **kwargs)
