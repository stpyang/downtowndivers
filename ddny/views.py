'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import get_template

from ddny.decorators import consent_required, warn_if_superuser

def contact_info(request):
    return render(request, 'ddny/contact_info.html')


def club_dues(request):
    return render(request, 'ddny/club_dues.html')

@warn_if_superuser
@login_required
@consent_required
def home(request):
    return render(request, 'ddny/home.html')


def privacy_policy(request):
    return render(request, 'ddny/privacy_policy.html')


def refund_policy(request):
    return render(request, 'ddny/refund_policy.html')

def oops(request, text_template, html_template, view, messages):
    '''In exceptional cases (no pun intended) send an e-mail'''
    context = {
        "oops_email": settings.OOPS_EMAIL,
        "current_user": request.user.username,
        "error_messages": messages,
    }
    text_content = get_template(text_template)
    html_content = get_template(html_template)
    warning = EmailMultiAlternatives(
        subject="DDNY automated warning: {0}".format(view),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.OOPS_EMAIL],
        body=text_content.render(context)
    )
    warning.attach_alternative(
        content=html_content.render(context),
        mimetype="text/html",
    )
    warning.send()
    return render(request, "ddny/oops.html", context)

