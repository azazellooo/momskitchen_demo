from django.urls import path
from KitchenWeb.views.views import (
    OrganizationsListView
)

app_name = 'organizations'

urlpatterns = [
    path("", OrganizationsListView.as_view(), name="list"),
]