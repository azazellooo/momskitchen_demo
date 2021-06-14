from rest_framework import serializers
from accounts.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['name', 'secondary_key', 'generate_link']
        read_only_fields = ['id']
