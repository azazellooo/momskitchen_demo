from django.urls import path
from accounts.tasks import one_time_transition, code_red_token
from accounts.views import UserProfileView, UserUpdateView, EmployeeTransactionHistoryView, ReviewListView

urlpatterns = [
    path('<uuid:token>/', UserProfileView.as_view(), name='profile'),
    path('', UserProfileView.as_view(), name='profile_distoken'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/transactions/', EmployeeTransactionHistoryView.as_view(), name='employee-transactions'),
    path('disposability/error/', one_time_transition, name='disposability_error'),
    path('invalid/token/', code_red_token, name='invalid_token'),
    path('reviews/', ReviewListView.as_view(), name='reviews_list')


]


