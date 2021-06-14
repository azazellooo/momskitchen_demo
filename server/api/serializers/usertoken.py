from rest_framework import serializers
from accounts.models import UserToken


class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserToken
        fields = ['id', 'key', 'user']
        read_only_fields = ['key', 'user']