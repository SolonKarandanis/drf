from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list_create_view, name='product-list'),
    path('create/', views.product_create_view, name='product-create'),
    path('<int:pk>/update/', views.product_update_view, name='product-update'),
    path('<int:pk>/delete/', views.product_delete_view, name='product-delete'),
    path('<int:pk>/', views.get_product, name='product-detail'),
]