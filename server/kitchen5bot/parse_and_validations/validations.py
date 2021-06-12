from accounts.models import Organization, Users
from django.core.exceptions import ObjectDoesNotExist


def is_organization(second_key):
    try:
        return Organization.objects.get(secondary_key=second_key)
    except ObjectDoesNotExist:
        return None

def is_user(user_id):
    try:
        return Users.objects.get(tg_user=user_id)
    except ObjectDoesNotExist:
        return None


def deep_len_validator(text):
    if len(text) == 43:
        return True
    else:
        return False