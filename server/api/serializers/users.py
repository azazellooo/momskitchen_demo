from rest_framework import serializers
from accounts.models import Employe


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employe
        fields = ['id', 'tg_user', 'organization_id', 'username', 'is_active']
        read_only_fields = ['tg_user', 'organization_id']




