from django.shortcuts import render

from accounts.models import UserToken, Employee
from datetime import datetime, timedelta
from django.contrib.sessions.backends.db import SessionStore
import pytz
from django.utils import timezone


def drop_time_token(token, key_session1):
    utc = pytz.UTC
    token_user = UserToken.objects.get(key=token)
    finish_time = token_user.created_at.replace(tzinfo=utc) + timedelta(minutes=60)
    now = timezone.now()
    if now >= finish_time:
        s = SessionStore(session_key=key_session1)
        s.delete()
        token_user.delete()

def validation_token(token):
    try:
        UserToken.objects.get(key=token)
        return True
    except:
        return False

def get_user(token):
    val_tok = UserToken.objects.get(key=token)
    user = val_tok.user
    return user


def one_time_transition(request):
    return render(request, 'accounts/one_time_transition_error.html')


def code_red_token(request):
    return render(request, 'accounts/code_red_token.html')






