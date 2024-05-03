from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.get_logged_in_user_rooms, name='logged-user-rooms'),
    path('rooms/user/<str:uuid>/', views.get_user_rooms, name='user-rooms'),
]
