from django.urls import path, include

from api.views import OrganizationDetailView, UsersApiView

app_name = 'api'

organization_api_urls = [
    path('<int:pk>', OrganizationDetailView.as_view(), name='detail')
]

users_api_urls = [
    path('<uuid:token>/', UsersApiView.as_view(), name='profile'),
]

urlpatterns = [
    path('organizations/', include(organization_api_urls)),
    path('profiles/', include(users_api_urls)),

]