from typing import List

from django.conf import settings
from django.db.models import Prefetch
from .models import Order, OrderItem, OrderManager

User = settings.AUTH_USER_MODEL


class OrderRepository:

    def _model_manager(self) -> OrderManager:
        return Order.objects

    def find_order_ids_with_is_shipped(self):
        return self._model_manager().get_queryset().order_ids_with_is_shipped()

    def find_users_orders(self, user: User) -> List[Order]:
        return self._model_manager().get_queryset().owned_by(user=user)

    def find_users_order_number(self, user: User) -> int:
        return self._model_manager().get_queryset().owned_by(user=user).count()

    def find_users_largest_order(self, user: User) -> float:
        return self._model_manager().get_queryset().owned_by(user=user).max_total_price()

    def find_users_sum_order_price(self, user: User) -> float:
        return self._model_manager().get_queryset().owned_by(user=user).sum_total_price()

    def find_total_sales_per_user(self) -> float:
        return self._model_manager().get_queryset().total_sales()

    def find_recendly_shipped_orders_by_supplier(self, user: User) -> List[Order]:
        return self._model_manager().get_queryset().supplied_by(user).recently_shipped()

    def find_received_orders_by_supplier(self, user: User) -> List[Order]:
        return self._model_manager().get_queryset().supplied_by(user).received()

    def place_order(self, buyer, supplier) -> Order:
        return self._model_manager().create_order(buyer, supplier)

    def update_order(self, order: Order) -> Order:
        return self._model_manager().update_order(order)

    def find_order_by_uuid(self, uuid: str) -> Order:
        return self._model_manager().get_queryset().by_uuid(uuid)

    def find_order_by_uuid_with_products(self, uuid: str, fetch_items: bool) -> Order:
        query = self._model_manager()
        if fetch_items:
            order_items_prefect = Prefetch('order_items', queryset=OrderItem.objects.select_related('product'))
            comments_prefetch = Prefetch('comments')
            query.prefetch_related(order_items_prefect, comments_prefetch)
        return query.get(uuid=uuid)

    def find_order_by_id(self, order_id: int, fetch_items: bool) -> Order:
        query = self._model_manager()
        if fetch_items:
            query.get_queryset().with_order_items()
        return query.get(pk=order_id)

    def find_order_by_id_with_products(self, order_id: int, fetch_items: bool) -> Order:
        query = self._model_manager()
        if fetch_items:
            order_items_prefect = Prefetch('order_items', queryset=OrderItem.objects.select_related('product'))
            comments_prefetch = Prefetch('comments')
            query.prefetch_related(order_items_prefect, comments_prefetch)
        return query.get(pk=order_id)

    def find_orders_by_requested_status(self, requested_status: str) -> List[Order]:
        return self._model_manager().get_queryset().by_status(requested_status)

    def find_order_item_by_uuid(self, uuid: str) -> OrderItem:
        return OrderItem.objects.get_queryset().with_product().by_uuid(uuid)

    def find_order_item_by_id(self, order_item_id: int) -> OrderItem:
        return OrderItem.objects.get_queryset().with_product().get(pk=order_item_id)

    def update_order_item(self, order_item: OrderItem) -> OrderItem:
        item = OrderItem.objects.update_item(order_item)
        return item

    def search_order_items(self, query: str, user: User = None) -> List[OrderItem]:
        return OrderItem.objects.get_queryset().fts_search(query, user)

    def initialize_order_item(self, product_id: int, order_id: int, product_name: str, sku: str, price: float, quantity: float, total_price: float):
        return OrderItem.objects.create_order_item(product_id, order_id, product_name, sku, price, quantity,
                                                   total_price)
