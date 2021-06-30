from django.urls import path, include

from KitchenWeb.views import GarnishCreateView
from KitchenWeb.views.organizations import (
    OrganizationsListView,
    OrganizationCreateView,
    OrganizationDetailUpdateView
)
from KitchenWeb.views.kitchen import (
    SupplementListView,
    SupplementCreateView,
    SupplementDetailUpdateView,
)
from KitchenWeb.views.position import (
    PositionCreateView,
    PositionListView,
)
from KitchenWeb.views.garnish import (
    GarnishListView,
    GarnishDetailUpdateView
)
from KitchenWeb.views.category import (
    CategoryListView,
    CategoryCreateView,
    CategoryDetailUpdateView
)
from KitchenWeb.views.additional import (
    AdditionalListView
)

app_name = 'kitchen'

organization_urls = [
    path("", OrganizationsListView.as_view(), name="organization-list"),
    path('create/', OrganizationCreateView.as_view(), name='organization-create'),
    path('<int:pk>/', OrganizationDetailUpdateView.as_view(), name='organization-detail-update')
]

kitchen_urls = [
    path('supplements/', SupplementListView.as_view(), name='supplement-list'),
    path('supplements/create/', SupplementCreateView.as_view(), name='create_supplement'),
    path('supplement/<int:pk>/detail_update/', SupplementDetailUpdateView.as_view(), name='detail_update_supplement'),
    path('position/create/', PositionCreateView.as_view(), name='create_position'),
    path('position/list/', PositionListView.as_view(), name='list_position'),
    path('garnish/list/', GarnishListView.as_view(), name='list_garnish'),
    path('garnish/<int:pk>/', GarnishDetailUpdateView.as_view(), name='garnish-detail-update'),
    path('categories/list/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/detail/<int:pk>/', CategoryDetailUpdateView.as_view(), name='category_update_detail')

]

urlpatterns = [
    path("organizations/", include(organization_urls)),
    path('kitchen/', include(kitchen_urls))
]
