from django.urls import path, include
from KitchenWeb.views.organizations import (
    OrganizationsListView
)
from KitchenWeb.views.kitchen import (
    SupplementListView,
    SupplementCreateView,
    SupplementDetailView,
    SupplementUpdateView,
)

app_name = 'kitchen'

organization_urls = [
    path("", OrganizationsListView.as_view(), name="organization-list"),
]

kitchen_urls = [
    path('supplements/', SupplementListView.as_view(), name='supplement-list'),
    path('supplements/create/', SupplementCreateView.as_view(), name='create_supplement'),
    path('supplement/<int:pk>', SupplementDetailView.as_view(), name='detail_supplement'),
    path('supplement/<int:pk>/update/', SupplementUpdateView.as_view(), name='update_supplement'),
]

urlpatterns = [
    path("organizations/", include(organization_urls)),
    path('kitchen/', include(kitchen_urls))
]
