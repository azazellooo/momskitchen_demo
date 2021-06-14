from django.urls import path, include

from api.views import OrganizationDetailView

app_name = 'api'

organization_api_urls = [
    path('<int:pk>', OrganizationDetailView.as_view(), name='detail')
]

urlpatterns = [
    path('organizations/', include(organization_api_urls)),

]