from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_user_orders, name='users-orders'),
    path('place-draft/', views.place_draft_orders, name='draft-orders'),
    path('comment/', views.post_order_comment, name='comment-order'),
    path('<str:uuid>/', views.get_order, name='fetch-order'),
    path('<str:uuid>/buyer-reject', views.order_buyer_rejected, name='order-buyer-reject'),
    path('<str:uuid>/supplier-reject', views.order_supplier_rejected, name='order-supplier-reject'),
    path('<str:uuid>/approve', views.order_approved, name='order-approve'),
    path('<str:uuid>/ship', views.order_shipped, name='order-ship'),
    path('<str:uuid>/receive', views.order_received, name='order-receive'),
]
