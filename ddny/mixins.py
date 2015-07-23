'''Copyright 2015 DDNY. All Rights Reserved.'''

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class WarnIfSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            messages.warning(request,
                             "With great power comes great responsibility. " + \
                    "Do you REALLY want to be logged in as a superuser?")
        return super(WarnIfSuperuserMixin, self).dispatch(
            request, *args, **kwargs)


class ConsentRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, "member") and not request.user.member.current_consent:
            return HttpResponseRedirect(reverse("consent_form"))
        return super(ConsentRequiredMixin, self).dispatch(
            request, *args, **kwargs)
