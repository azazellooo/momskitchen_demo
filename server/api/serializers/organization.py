from rest_framework import serializers
from accounts.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['name', 'payment', 'address', 'bonus_activation', 'leave_review']
        read_only_fields = ['id', 'secondary_key', 'generate_link']
