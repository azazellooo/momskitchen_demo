from django.shortcuts import render

from accounts.models import UserToken, Employee
from datetime import datetime, timedelta
from django.contrib.sessions.backends.db import SessionStore
import pytz
from django.utils import timezone
import json


def drop_time_token(token, key_session1):
    utc = pytz.UTC
    token_user = UserToken.objects.get(key=token)
    finish_time = token_user.created_at.replace(tzinfo=utc) + timedelta(hours=36)
    now = timezone.now()
    if now >= finish_time:
        s = SessionStore(session_key=key_session1)
        s.delete()
        token_user.delete()


def validation_token(token):
        return UserToken.objects.filter(key=token).exists()


def get_user(token):
    val_tok = UserToken.objects.get(key=token)
    user = val_tok.user
    return user


def one_time_transition(request):
    return render(request, 'accounts/one_time_transition_error.html')


def code_red_token(request):
    return render(request, 'accounts/code_red_token.html')


def extra_price_parcer(extra_price):
    extra_price_dict = json.loads(extra_price)
    total = 0
    for key, value in extra_price_dict:
        total += value['price']
    return total


def create_json_portions(position, garnish, additional):
    total_sum_price = 0
    to_json = {}
    offering_portion = position['portion']
    offering_price = position['price']
    to_json['Position'] = {'portion': f'{offering_portion}', 'price': f'{offering_price}'}
    total_sum_price += int(offering_price)
    if garnish != None:
        price_garnish = garnish['price']
        garnish_portion = garnish['portion']
        garnish_name = garnish['name']
        to_json['Garnish'] = {'portion': f'{garnish_portion}', 'price': f'{price_garnish}', 'name': f'{garnish_name}'}
        total_sum_price += int(price_garnish)
    if additional != None:
        price_additional = additional['price']
        additional_portion = additional['portion']
        additional_name = additional['name']
        to_json['Additional'] = {'portion': f'{additional_portion}',
                                 'price': f'{price_additional}', 'name': f'{additional_name}'}
        total_sum_price += int(price_additional)
    to_json['total_price'] = str(total_sum_price)
    return to_json

def json_parcer(json_to_portions):
    json_parce = json.loads(json_to_portions)
    return json_parce











