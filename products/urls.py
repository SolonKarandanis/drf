from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_products, name='product-list'),
    path('supplier/', views.get_all_supplier_products, name='product-supplier-list'),
    path('create/', views.create_product, name='product-create'),
    path('comment/', views.post_product_comment, name='comment-product'),
    path('search/', views.search_products, name='search-products'),
    path('categories/', views.get_categories_with_totals, name='product-categories'),
    path('brands/', views.get_brands_with_totals, name='product-brands'),
    path('sizes/', views.get_sizes_with_totals, name='product-sizes'),
    # path('<str:uuid>/update/', views.product_update_view, name='product-update'),
    # path('<str:uuid>/delete/', views.product_delete_view, name='product-delete'),
    path('<str:uuid>/', views.get_product, name='product-detail'),
    path('supplier/<str:uuid>/', views.get_supplier_product, name='product-supplier-detail'),
]