from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_notifications, name='notifications-list'),
    path('unread-count/', views.get_unread_count, name='notifications-unread-count'),
    path('read/', views.mark_as_read, name='notifications-mark-read'),
]
