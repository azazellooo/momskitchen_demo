from rest_framework import serializers
from accounts.models import Users


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['id', 'tg_user', 'organization_id', 'username', 'is_active']
        read_only_fields = ['tg_user', 'organization_id']




