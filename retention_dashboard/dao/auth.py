from django.conf import settings
from uw_saml.utils import is_member_of_group


def is_omad_authorized(request):
    return is_member_of_group(request, settings.OMAD_USERS_GROUP)


def is_eop_authorized(request):
    return is_member_of_group(request, settings.EOP_USERS_GROUP)


def is_international_authorized(request):
    return is_member_of_group(request, settings.INTERNATIONAL_USERS_GROUP)


def get_type_authorizations(request):
    types = []
    if is_omad_authorized(request):
        types.append("OMAD")
    if is_eop_authorized(request):
        types.append("EOP")
    if is_international_authorized(request):
        types.append("International")
    return types
