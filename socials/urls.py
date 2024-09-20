from django.urls import path

from socials.views import find_users_socials, create_user_socials, delete_user_social

urlpatterns = [
    path('users/<str:uuid>/', find_users_socials,  name='users-socials'),
    path('users/<str:uuid>/create', create_user_socials, name='create-users-socials'),
    path('users/<str:uuid>/delete/<int:id>', delete_user_social, name='delete-users-social'),
]
