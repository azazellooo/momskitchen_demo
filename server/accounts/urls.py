from django.contrib import admin
from django.urls import path

from accounts.views import UserProfileView, UserUpdateView, EmployeeTransactionHistoryView

urlpatterns = [
    path('<uuid:token>/', UserProfileView.as_view(), name='profile'),
    path('', UserProfileView.as_view(), name='profile_distoken'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/transactions/', EmployeeTransactionHistoryView.as_view(), name='employee-transactions')
]


