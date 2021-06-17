from django.contrib import admin
from django.urls import path

from accounts.views import UserProfileView, UserUpdateView

urlpatterns = [
    path('<uuid:token>/', UserProfileView.as_view(), name='profile'),
    path('update/<uuid:token>/', UserUpdateView.as_view(), name='user_update'),
]


