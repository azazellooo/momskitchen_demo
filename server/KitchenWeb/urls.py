from django.urls import path, include

from KitchenWeb.views.additional import (
    AdditionalListView,
    AdditionalCreateView,
    AdditionalDetailUpdateView
)
from KitchenWeb.views.category import (
    CategoryListView,
    CategoryCreateView,
    CategoryDetailUpdateView
)
from KitchenWeb.views.garnish import (
    GarnishListView,
    GarnishDetailUpdateView
)
from KitchenWeb.views.garnish_create import (
    GarnishCreateView
)
from KitchenWeb.views.kitchen import (
    SupplementListView,
    SupplementCreateView,
    SupplementDetailUpdateView,
)
from KitchenWeb.views.offering import (
    OfferingCreateView,
    OfferingListView,
    OfferingDetailUpdateView
)
from KitchenWeb.views.organizations import (
    OrganizationsListView,
    OrganizationCreateView,
    OrganizationDetailUpdateView,
    OrganizationBalancePageView
)
from KitchenWeb.views.position import (
    PositionCreateView,
    PositionListView, PositionDetailUpdateView,
)
from KitchenWeb.views.orders import OrderListView
from KitchenWeb.views.menu import OfferingListViewForDate

app_name = 'kitchen'

organization_urls = [
    path("", OrganizationsListView.as_view(), name="organization-list"),
    path('create/', OrganizationCreateView.as_view(), name='organization-create'),
    path('<int:pk>/', OrganizationDetailUpdateView.as_view(), name='organization-detail-update'),
    path('balance/<int:pk>/', OrganizationBalancePageView.as_view(), name='organization-balance')
]

kitchen_urls = [
    path('supplements/', SupplementListView.as_view(), name='supplement-list'),
    path('supplements/create/', SupplementCreateView.as_view(), name='create_supplement'),
    path('supplement/<int:pk>/detail_update/', SupplementDetailUpdateView.as_view(), name='detail_update_supplement'),
    path('position/create/', PositionCreateView.as_view(), name='create_position'),
    path('position/list/', PositionListView.as_view(), name='list_position'),
    path('position/<int:pk>/', PositionDetailUpdateView.as_view(), name='detail_update_position'),
    path('garnish/list/', GarnishListView.as_view(), name='list_garnish'),
    path('garnish/create/', GarnishCreateView.as_view(), name='create_garnish'),
    path('garnish/<int:pk>/', GarnishDetailUpdateView.as_view(), name='garnish-detail-update'),
    path('categories/list/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/detail/<int:pk>/', CategoryDetailUpdateView.as_view(), name='category_update_detail'),
    path('additional/list/', AdditionalListView.as_view(), name='additional_list'),
    path('additional/create/', AdditionalCreateView.as_view(), name='additional_create'),
    path('additional/<int:pk>/', AdditionalDetailUpdateView.as_view(), name='additional_detail_update'),
    path('offering/create/', OfferingCreateView.as_view(), name='offering_create'),
    path('offering/list/', OfferingListView.as_view(), name='offering_list'),
    path('offering/<int:pk>/', OfferingDetailUpdateView.as_view(), name='offering-detail'),
    path('offering/<str:date>/<uuid:token>/', OfferingListViewForDate.as_view(), name='offering-list-for-date')

]

urlpatterns = [
    path("organizations/", include(organization_urls)),
    path('kitchen/', include(kitchen_urls)),
]
