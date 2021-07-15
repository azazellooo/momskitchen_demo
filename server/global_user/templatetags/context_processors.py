from django import template
from django.urls import reverse

from accounts.tasks import get_user

register = template.Library()


def check_admin(request, *args, **kwargs):
    if request.path.startswith(reverse('admin:index')):
        return {}
    else:
        token = request.session['token']
        user = get_user(token)
        if user.is_admin:
            return {'admin':True}
        else:
            return {'admin':False}


