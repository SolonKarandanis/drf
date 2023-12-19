from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_user_orders, name='users-orders'),
    path('place-draft/', views.place_draft_orders, name='draft-orders'),
    path('<str:uuid>/', views.get_order, name='fetch-order'),
]
