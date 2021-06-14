from django.contrib import admin
from django.urls import path

from accounts.views import UserProfileView

urlpatterns = [
    path('profiles/<uuid:token>/', UserProfileView.as_view(), name='profile'),
]


