from django.urls import path

from socials.views import find_users_socials

urlpatterns = [
    path('users/<int:user_id>/', find_users_socials,  name='users-socials'),
]