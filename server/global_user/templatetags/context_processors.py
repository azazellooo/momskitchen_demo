from django import template
from django.urls import reverse

from KitchenWeb.models import Cart
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


def offering_in_cart(request, *args, **kwargs):
    if request.path.startswith(reverse('admin:index')):
        return {}
    token = request.session['token']
    user = get_user(token)
    carts = Cart.objects.filter(user=user, is_confirmed=False)
    return {'carts': carts}


