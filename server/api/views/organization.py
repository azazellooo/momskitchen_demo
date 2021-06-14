from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Organization
from api.serializers.organization import OrganizationSerializer


class OrganizationDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Organization, pk=pk)

    def get(self, request, pk):
        organization = self.get_object(pk)
        response_data = OrganizationSerializer(organization).data
        return Response(data=response_data)
