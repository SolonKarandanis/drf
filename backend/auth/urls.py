from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import get_all_users, create_user, get_user

urlpatterns = [
    path('', obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/', get_all_users,  name='get-users'),
    path('users/create/', create_user,  name='create-user'),
    path('users/<int:pk>/', get_user,  name='get-user'),
]
