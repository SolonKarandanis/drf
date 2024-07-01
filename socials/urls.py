from django.urls import path

from socials.views import find_users_socials

urlpatterns = [
    path('users/<str:uuid>/', find_users_socials,  name='users-socials'),
]