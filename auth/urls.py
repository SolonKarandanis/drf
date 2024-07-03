from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import get_all_users, create_user, get_user, get_account, run_task, get_status, get_all_groups, \
    search_users, activate_user_account, deactivate_user_account, delete_user_account, upload_cv, upload_profile_image, \
    get_user_statuses, get_user_image

urlpatterns = [
    path('', obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/', get_all_users,  name='get-users'),
    path('users/activate', activate_user_account,  name='activate-user-account'),
    path('users/deactivate', deactivate_user_account, name='deactivate-user-account'),
    path('users/delete', delete_user_account, name='delete-user-account'),
    path('users/search', search_users,  name='search-users'),
    path('users/create/', create_user,  name='create-user'),
    path('users/account/', get_account,  name='get-account'),
    path('users/groups/', get_all_groups, name='get-groups'),
    path('users/statuses/', get_user_statuses, name='get-statuses'),
    path('users/<str:uuid>/', get_user, name='get-user'),
    path('users/<str:uuid>/image/', get_user_image,  name='get-user-image'),
    path('users/<str:uuid>/upload-cv/', upload_cv,  name='upload-cv'),
    path('users/<str:uuid>/upload-profile-image/', upload_profile_image,  name='upload-profile-image'),
    path('task/', run_task,  name='run_task'),
    path('task/<str:task_id>/', get_status,  name='get_status'),
]
