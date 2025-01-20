from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_products, name='product-list'),
    path('supplier/', views.get_all_supplier_products, name='product-supplier-list'),
    path('create/', views.create_product, name='product-create'),
    path('comment/', views.post_product_comment, name='comment-product'),
    path('search/', views.search_products, name='search-products'),
    path('categories/', views.get_all_categories, name='all-categories'),
    path('brands/', views.get_all_brands, name='all-brands'),
    path('all-attributes/', views.get_all_attributes, name='all-attributes'),
    path('sizes/', views.get_all_sizes, name='all-sizes'),
    path('colours/', views.get_all_colours, name='all-colours'),
    path('genders/', views.get_all_genders, name='all-genders'),
    path('categories/totals/', views.get_categories_with_totals, name='product-categories'),
    path('brands/totals/', views.get_brands_with_totals, name='product-brands'),
    path('sizes/totals/', views.get_sizes_with_totals, name='product-sizes'),
    # path('<str:uuid>/update/', views.product_update_view, name='product-update'),
    path('similar-products/', views.get_similar_products, name='product-detail-similar-products'),
    path('<str:uuid>/', views.get_product, name='product-detail'),
    path('<str:uuid>/update/', views.update_product, name='update-product'),
    path('<str:uuid>/images/', views.get_product_images, name='product-detail-images'),
    path('<str:uuid>/similar-products/', views.get_similar_products_by_uuid,
         name='product-detail-similar-products-by-id'),
    path('<str:uuid>/attributes/', views.get_product_attributes, name='product-attributes'),
    path('supplier/<str:uuid>/', views.get_supplier_product, name='product-supplier-detail'),
]