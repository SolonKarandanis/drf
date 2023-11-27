from django.conf import settings
from .models import Order
User = settings.AUTH_USER_MODEL

class OrderRepository:

    def find_order_ids_with_is_shipped(self):
        return Order.objects.get_queryset().order_ids_with_is_shipped()

    def find_users_order_number(self, user: User) -> int:
        return Order.objects.get_queryset().owned_by(user=user).count()

    def find_users_largest_order(self, user: User):
        return Order.objects.get_queryset().owned_by(user=user).max_total_price()

    def find_users_sum_order_price(self, user: User):
        return Order.objects.get_queryset().owned_by(user=user).sum_total_price()
    