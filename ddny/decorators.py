'''Copyright 2015 DDNY. All Rights Reserved.'''

import functools

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def warn_if_superuser(view_func):
    '''decorator to warn if the the superuser is logged in'''
    @functools.wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            messages.warning(request,
                             "With great power comes great responsibility. " + \
                    "Do you REALLY want to be logged in as a superuser?")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def consent_required(view_func):
    '''decorator to required a current consent forms'''
    @functools.wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, "member") and not request.user.member.current_consent:
            return HttpResponseRedirect(reverse("consent_form"))
        return view_func(request, *args, **kwargs)
    return _wrapped_view
