from django.urls import path
from . import views

urlpatterns = [
    path('place-draft/', views.place_draft_orders, name='draft-orders'),
    path('<str:uuid>/', views.get_order, name='fetch-order'),
]
