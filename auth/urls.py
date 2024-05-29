from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import get_all_users, create_user, get_user, get_account, run_task, get_status, get_all_groups, \
    search_users, change_user_account_status

urlpatterns = [
    path('', obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/', get_all_users,  name='get-users'),
    path('users/status', change_user_account_status,  name='change-users-status'),
    path('users/search', search_users,  name='search-users'),
    path('users/create/', create_user,  name='create-user'),
    path('users/account/', get_account,  name='get-account'),
    path('users/<str:uuid>/', get_user, name='get-user'),
    path('users/groups/', get_all_groups,  name='get-groups'),
    path('task/', run_task,  name='run_task'),
    path('task/<str:task_id>/', get_status,  name='get_status'),
]
