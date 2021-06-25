from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from accounts.models import Users, UserToken
from django.contrib.auth import logout
import datetime
import pytz
from django.utils import timezone
from django.http import HttpResponse



class CustomAuthMiddleware(MiddlewareMixin):

    def process_request(self, request, **kwargs):
        try:
            myToken = request.session.get('token')
            token = UserToken.objects.get(key=myToken)
            print(token)
            utc = pytz.UTC
            finish_time = token.created_at.replace(tzinfo=utc) + datetime.timedelta(minutes=30)
            now = timezone.now()
            if now >= finish_time:
                # delete token from session & clear session
                print('old')
                return HttpResponse('Unauthorized', status=401)
            else:
                try:
                    user = token.user
                    return
                except:
                    print('no user')
                    return HttpResponse('Unauthorized', status=401)
        except UserToken.DoesNotExist:
            print('no token')
            return HttpResponse('Unauthorized', status=401)

