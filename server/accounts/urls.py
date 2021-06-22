from django.contrib import admin
from django.urls import path

from accounts.views import UserProfileView, UserUpdateView

urlpatterns = [
    path('<uuid:token>/', UserProfileView.as_view(), name='profile'),
    path('', UserProfileView.as_view(), name='profile_distoken'),
    path('update/', UserUpdateView.as_view(), name='user_update')
]


