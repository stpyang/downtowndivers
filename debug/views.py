'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ddny.decorators import consent_required, warn_if_superuser


@warn_if_superuser
@consent_required
@login_required
def blend_tests(request):
    return render(request, 'debug/blend_tests.html')


@warn_if_superuser
@consent_required
@login_required
def fill_tests(request):
    return render(request, 'debug/fill_tests.html')
