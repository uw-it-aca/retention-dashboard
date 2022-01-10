# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from uw_saml.utils import is_member_of_group


def is_premajor_authorized(request):
    return is_member_of_group(request, settings.PREMAJOR_USERS_GROUP)


def is_eop_authorized(request):
    return is_member_of_group(request, settings.EOP_USERS_GROUP)


def is_international_authorized(request):
    return is_member_of_group(request, settings.INTERNATIONAL_USERS_GROUP)


def is_iss_authorized(request):
    return is_member_of_group(request, settings.ISS_USERS_GROUP)


def is_tacoma_authorized(request):
    return is_member_of_group(request, settings.TACOMA_USERS_GROUP)


def is_athletic_authorized(request):
    return is_member_of_group(request, settings.ATHLETIC_USERS_GROUP)


def get_type_authorizations(request):
    types = []
    if is_premajor_authorized(request):
        types.append("Premajor")
    if is_eop_authorized(request):
        types.append("EOP")
    if is_international_authorized(request):
        types.append("International")
    if is_iss_authorized(request):
        types.append("ISS")
    if is_tacoma_authorized(request):
        types.append("Tacoma")
    if is_athletic_authorized(request):
        types.append("Athletics")
    return types
