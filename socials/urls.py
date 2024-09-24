from django.urls import path

from socials.views import find_users_socials, create_user_socials, delete_user_social, delete_user_social_by_ids, \
    delete_all_user_socials

urlpatterns = [
    path('users/<str:uuid>/', find_users_socials,  name='users-socials'),
    path('users/<str:uuid>/create/', create_user_socials, name='create-users-socials'),
    path('users/<str:uuid>/delete/<int:id>', delete_user_social, name='delete-users-social'),
    path('users/<str:uuid>/delete/', delete_user_social_by_ids, name='delete-users-social-by-ids'),
    path('users/<str:uuid>/clear/', delete_all_user_socials, name='delete-all-user-socials'),
]
