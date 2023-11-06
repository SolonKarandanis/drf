from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_user_cart, name='user-cart'),
]
