from django.urls import path, include
from KitchenWeb.views.organizations import (
    OrganizationsListView,
    OrganizationCreateView
)
from KitchenWeb.views.kitchen import (
    SupplementListView,
    SupplementCreateView,
    SupplementDetailView,
    SupplementUpdateView,
)
from KitchenWeb.views.position import (
    PositionCreateView,
    PositionListView
)
app_name = 'kitchen'

organization_urls = [
    path("", OrganizationsListView.as_view(), name="organization-list"),
    path('create/', OrganizationCreateView.as_view(), name='organization-create')
]

kitchen_urls = [
    path('supplements/', SupplementListView.as_view(), name='supplement-list'),
    path('supplements/create/', SupplementCreateView.as_view(), name='create_supplement'),
    path('supplement/<int:pk>', SupplementDetailView.as_view(), name='detail_supplement'),
    path('supplement/<int:pk>/update/', SupplementUpdateView.as_view(), name='update_supplement'),
    path('position/create/', PositionCreateView.as_view(), name='create_position'),
    path('position/list/', PositionListView.as_view(), name='list_position')
]

urlpatterns = [
    path("organizations/", include(organization_urls)),
    path('kitchen/', include(kitchen_urls))
]
