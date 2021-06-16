from django.urls import path, include
from KitchenWeb.views.organizations import (
    OrganizationsListView
)
from KitchenWeb.views.kitchen import SupplementListView

app_name = 'kitchen'

organization_urls = [
    path("", OrganizationsListView.as_view(), name="organization-list"),
]

kitchen_urls = [
    path('supplements/', SupplementListView.as_view(), name='supplement-list')
]

urlpatterns = [
    path("organizations/", include(organization_urls)),
    path('kitchen/', include(kitchen_urls))
]
