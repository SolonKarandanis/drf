from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_products, name='product-list'),
    path('supplier/', views.get_all_supplier_products, name='product-supplier-list'),
    path('create/', views.create_product, name='product-create'),
    path('<int:pk>/update/', views.product_update_view, name='product-update'),
    path('<int:pk>/delete/', views.product_delete_view, name='product-delete'),
    path('<int:pk>/', views.get_product, name='product-detail'),
    path('supplier/<int:pk>/', views.get_supplier_product, name='product-supplier-detail'),
]