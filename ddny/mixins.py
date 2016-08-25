'''Copyright 2016 DDNY. All Rights Reserved.'''

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
        if hasattr(request.user, "member") and \
            not request.user.member.honorary_member and \
            not request.user.member.current_consent:
            return HttpResponseRedirect(reverse("consent_form"))
        return super(ConsentRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class SortableMixin(object):
    """
    Allows sorting off of properties.
    """
    default_sort_params = ["pk"]

    def get_sort_params(self):
        sort_params = self.default_sort_params
        query_params = self.request.GET.get("sort_by", "")
        if query_params:
            sort_params = [param for param in query_params.split(",") if param]
        return sort_params

    def get_queryset(self):
        sort_by = self.get_sort_params()
        qs = super(SortableMixin, self).get_queryset()
        return qs.order_by(*sort_by)

    def get_context_data(self, *args, **kwargs):
        context = super(SortableMixin, self).get_context_data(*args, **kwargs)
        sort_params = self.get_sort_params()
        context.update({
            "sort_params": sort_params
        })
        return context
