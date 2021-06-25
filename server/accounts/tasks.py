
from accounts.models import UserToken
from datetime import datetime, timedelta
from django.contrib.sessions.backends.db import SessionStore
import pytz
from django.utils import timezone

def drop_time_token(token, key_session1):
    utc = pytz.UTC
    token_user = UserToken.objects.get(key=token)
    finish_time = token_user.created_at.replace(tzinfo=utc) + timedelta(minutes=1)
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




# @shared_task
# def add(x, y):
#     return x + y
#
#
# @shared_task
# def mul(x, y):
#     return x * y
#
#
# @shared_task
# def xsum(numbers):
#     return sum(numbers)
#
#
# @shared_task
# def count_widgets():
#     return Widget.objects.count()
#
#
# @shared_task
# def rename_widget(widget_id, name):
#     w = Widget.objects.get(id=widget_id)
#     w.name = name
#     w.save()