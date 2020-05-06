'''Copyright 2016 DDNY. All Rights Reserved.'''

from abc import abstractmethod
from datetime import date

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse

from ddny_calendar.models import Event
from fillstation.models import Fill, Prepay
from registration.models import Member
from .core import cash
from .decorators import consent_required, warn_if_superuser


def __calculate_prepaid(member):
    prepaid = Prepay.objects.filter(member=member)
    if prepaid.count():
        return prepaid.aggregate(Sum('amount')).get('amount__sum')
    return cash(0)


class AbstractActionMixin():
    '''set a message of if an object (eg Tank, Spec, Member) is created or saved'''

    @property
    @abstractmethod
    def success_msg(self):
        '''message to display on successful update'''
        return NotImplemented

    @property
    @abstractmethod
    def cancel_msg(self):
        '''message to display on cancellation of update'''
        return NotImplemented

    @property
    @abstractmethod
    def cancel_url(self):
        '''url to redirect to on cancellation of update'''
        return NotImplemented

    def form_valid(self, form):
        '''https://docs.djangoproject.com/en/2.2/ref/class-based-views/mixins-editing/
        #django.views.generic.edit.FormMixin.form_valid'''
        messages.info(self.request, self.success_msg)
        return super(AbstractActionMixin, self).form_valid(form)

    def forms_valid(self, forms, inlines):
        '''https://docs.djangoproject.com/en/2.2/ref/class-based-views/mixins-editing/
        #django.views.generic.edit.FormMixin.form_valid'''
        messages.info(self.request, self.success_msg)
        return super(AbstractActionMixin, self).forms_valid(forms, inlines)

    def post(self, request, *args, **kwargs):
        '''Constructs a form, checks the form for validity, and handles it accordingly.'''
        if 'cancel' in request.POST:
            messages.warning(self.request, self.cancel_msg)
            return HttpResponseRedirect(self.cancel_url)
        return super(AbstractActionMixin, self).post(request, *args, **kwargs)


def contact_info(request):
    '''basic contact info for the club'''
    return render(request, 'ddny/contact_info.html')


def club_dues(request):
    '''club dues information'''
    return render(request, 'ddny/club_dues.html')


@warn_if_superuser
@consent_required
@login_required
def home(request):
    '''home page for all members '''
    prepaid_balance = cash(0)
    unpaid_fills_balance = cash(0)
    if hasattr(request.user, 'member'):
        prepaid_balance = __calculate_prepaid(request.user.member)
        unpaid_fills = Fill.objects.unpaid().filter(bill_to=request.user.member)
        if unpaid_fills.count():
            unpaid_fills_balance = unpaid_fills.aggregate(Sum('total_price'))
            unpaid_fills_balance = unpaid_fills_balance.get('total_price__sum')
            unpaid_fills_balance = cash(unpaid_fills_balance)
    total_balance = prepaid_balance - unpaid_fills_balance

    event_array = map(
        lambda event: {
            'id': event.id,
            'title': event.title,
            'start': event.start_date.strftime('%Y-%m-%d'),
            'end': event.end_date.strftime('%Y-%m-%d'),
        },
        Event.objects.all()
    )

    upcoming_event_array = Event.objects.filter(show_on_homepage=True, end_date__gt=date.today())
    upcoming_events = map(
        lambda event: {
            'dates': event.get_dates(),
            'title': event.title,
        },
        upcoming_event_array,
    )
    upcoming_event_ids = map(
        lambda event: event.id,
        upcoming_event_array,
    )

    member_balance_info = []
    if hasattr(request.user, 'member') and request.user.member.is_treasurer:
        for member in Member.objects.all():
            if member.autopay_fills:
                continue
            member_prepaid_balance = __calculate_prepaid(member)

            member_unpaid_fills_balance = cash(0)
            member_unpaid_fills = Fill.objects.unpaid().filter(bill_to=member)
            if member_unpaid_fills.count():
                member_unpaid_fills_balance = member_unpaid_fills.aggregate(Sum('total_price'))
                member_unpaid_fills_balance = member_unpaid_fills_balance.get('total_price__sum')
                member_unpaid_fills_balance = cash(member_unpaid_fills_balance)
            member_total_balance = member_prepaid_balance - member_unpaid_fills_balance

            member_info = {}
            member_info['member'] = member
            member_info['prepaid_balance'] = member_prepaid_balance
            member_info['unpaid_fills_balance'] = member_unpaid_fills_balance
            member_info['total_balance'] = member_total_balance
            member_balance_info.append(member_info)

    context = {
        'prepaid_balance': prepaid_balance,
        'unpaid_fills_balance': unpaid_fills_balance,
        'total_balance': total_balance,
        'event_array': list(event_array),
        'upcoming_events': upcoming_events,
        'upcoming_event_ids': list(upcoming_event_ids),
        'add_event': reverse('ddny_calendar:add_event'),
        'delete_event': reverse('ddny_calendar:delete_event'),
        'update_event': reverse('ddny_calendar:update_event'),
        'member_balance_info': member_balance_info,
    }
    return render(request, 'ddny/home.html', context)


def privacy_policy(request):
    '''obligatory privacy policy'''
    return render(request, 'ddny/privacy_policy.html')


def refund_policy(request):
    '''obligatory refund policy'''
    return render(request, 'ddny/refund_policy.html')


def oops(request, text_template, html_template, view, error_messages):
    '''In exceptional cases (no pun intended) send an e-mail'''
    context = {
        'oops_email': settings.OOPS_EMAIL,
        'current_user': request.user.username,
        'error_messages': error_messages,
    }
    text_content = get_template(text_template)
    html_content = get_template(html_template)
    warning = EmailMultiAlternatives(
        subject='DDNY automated warning: {0}'.format(view),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.OOPS_EMAIL],
        body=text_content.render(context)
    )
    warning.attach_alternative(
        content=html_content.render(context),
        mimetype='text/html',
    )
    warning.send()
    return render(request, 'ddny/oops.html', context)
