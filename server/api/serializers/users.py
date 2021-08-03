from rest_framework import serializers
from accounts.models import Employee


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['id', 'tg_username', 'organization_id', 'username', 'is_active']
        read_only_fields = ['tg_username', 'organization_id']




