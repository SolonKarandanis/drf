from typing import List

from django.conf import settings
from .models import Order, OrderItem
User = settings.AUTH_USER_MODEL

class OrderRepository:

    def find_order_ids_with_is_shipped(self):
        return Order.objects.get_queryset().order_ids_with_is_shipped()

    def find_users_order_number(self, user: User) -> int:
        return Order.objects.get_queryset().owned_by(user=user).count()

    def find_users_largest_order(self, user: User) -> float:
        return Order.objects.get_queryset().owned_by(user=user).max_total_price()

    def find_users_sum_order_price(self, user: User) -> float:
        return Order.objects.get_queryset().owned_by(user=user).sum_total_price()

    def find_total_sales_per_user(self) -> float:
        return Order.objects.get_queryset().total_sales()

    def find_recendly_shipped_orders_by_supplier(self, user: User) -> List[Order]:
        return Order.objects.get_queryset().supplied_by(user).recently_shipped()

    def find_received_orders_by_supplier(self, user: User) -> List[Order]:
        return Order.objects.get_queryset().supplied_by(user).received()

    def place_order(self, buyer, supplier) -> Order:
        return Order.objects.create_order(buyer, supplier)

    def update_order(self, order: Order) -> Order:
        return Order.objects.update_order(order)

    def find_order_by_uuid(self, uuid: str) -> Order:
        return Order.objects.get_queryset().by_uuid(uuid)

    def find_order_by_id(self, order_id: int) -> Order:
        return Order.objects.get_queryset().get(pk=order_id)

    def find_orders_by_requested_status(self, requested_status: str) -> List[Order]:
        return Order.objects.get_queryset().by_status(requested_status)

    def update_order_item(self, order_item: OrderItem) -> OrderItem:
        item = OrderItem.objects.update_item(order_item)
        return item

    def search_order_items(self, query: str, user: User = None) -> List[OrderItem]:
        return OrderItem.objects.get_queryset().fts_search(query, user)
