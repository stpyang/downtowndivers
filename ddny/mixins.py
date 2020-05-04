'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


class WarnIfSuperuserMixin():  # pylint: disable=too-few-public-methods
    '''mixin to warn if the the superuser is logged in'''
    def dispatch(self, request, *args, **kwargs):
        '''warn if the superuser is logged in'''
        if request.user.is_superuser:
            messages.warning(request,
                             "With great power comes great responsibility. " +
                             "Do you REALLY want to be logged in as a " +
                             "superuser?")
        return super(WarnIfSuperuserMixin, self).dispatch(
            request, *args, **kwargs)


class ConsentRequiredMixin():  # pylint: disable=too-few-public-methods
    '''mixin to require a current consent form'''
    def dispatch(self, request, *args, **kwargs):
        '''require a current consent form'''
        if hasattr(request.user, "member") and \
            not request.user.member.honorary_member and \
                not request.user.member.current_consent:
            return HttpResponseRedirect(reverse("consent_form"))
        return super(ConsentRequiredMixin, self).dispatch(
            request, *args, **kwargs)
