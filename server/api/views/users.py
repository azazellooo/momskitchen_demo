from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Employee, UserToken
from api.serializers.users import UsersSerializer


class UsersApiView(APIView):
    def get_object(self, request, **kwargs):
        self.user = get_object_or_404(UserToken, key=kwargs['token'])
        return get_object_or_404(Employee, user_token=self.user)

    def get(self, request, **kwargs):
        user = self.get_object(request, **kwargs)
        response_data = UsersSerializer(user).data
        return Response(data=response_data)

    def put(self, request, format=None, **kwargs):
        user = self.get_object(request, **kwargs)
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors.HTTP_204_NO_CONTENT)
