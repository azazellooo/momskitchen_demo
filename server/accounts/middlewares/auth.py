from django.utils.deprecation import MiddlewareMixin
from accounts.models import Employee, UserToken
import datetime
import pytz
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.sessions.backends.db import SessionStore


class CustomAuthMiddleware(MiddlewareMixin):


    @staticmethod
    def get_user_token(token):
        try:
            return UserToken.objects.get(key=token)
        except UserToken.DoesNotExist:
            return None


    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if callback.__name__ == 'UserProfileView' or callback.__name__ == 'handle_bot_request' or 'admin' in request.path:
            return
        else:
            session_token = request.session.get('token', None)
            if session_token:
                token = self.get_user_token(session_token)
                if token:
                    utc = pytz.UTC
                    finish_time = token.created_at.replace(tzinfo=utc) + datetime.timedelta(minutes=60)
                    now = timezone.now()
                    if now >= finish_time:
                        session_data = SessionStore(session_key=request.session.session_key)
                        session_data.delete()
                        token.delete()
                        return HttpResponse('Unauthorized', status=401)
                    else:
                        try:
                            user = token.user
                            return
                        except Employee.DoesNotExist:
                            return HttpResponse('Unauthorized', status=401)
                else:
                    return HttpResponse('Unauthorized', status=401)
            else:
                return HttpResponse('Unauthorized', status=401)