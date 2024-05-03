from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_user_cart, name='user-cart'),
    path('items/', views.add_cart_items, name='add-items'),
    path('items/update/', views.update_quantities, name='update-quantity'),
    path('items/delete/', views.delete_cart_items, name='delete-items'),
    path('clear/', views.clear_cart, name='clear-cart'),
    path('order/<str:order_uuid>/', views.add_order_to_cart, name='add-order-to-cart'),
    path('order/item/<str:order_item_uuid>/', views.add_order_item_to_cart, name='add-order-item-to-cart'),
]
