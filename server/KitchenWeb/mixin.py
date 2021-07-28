from django.http import HttpResponse
from accounts.tasks import get_user


class PermissionMixin():
    def dispatch(self, request, *args, **kwargs):
        if get_user(request.session['token']).is_admin:
            return super(PermissionMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('Unauthorized', status=401)
