from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.get_user_wishlist_items, name='user-wishlist-items'),
    path('items/', views.add_to_wishlist, name='add-items'),
    path('items/delete/', views.remove_wishlist_item, name='delete-items'),
]
