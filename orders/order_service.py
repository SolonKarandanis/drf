from typing import List
from django.conf import settings
from django.db import transaction
from django.utils import timezone
import logging
from .models import Order, OrderItem
from .order_repository import OrderRepository
from cart.cart_service import CartService
from cart.models import Cart
from comments.comment_repository import CommentRepository

from .serializers import PostOrderComment

logger = logging.getLogger('django')
User = settings.AUTH_USER_MODEL
order_repo = OrderRepository()
comment_repo = CommentRepository()
cart_service = CartService()


class OrderService:

    @transaction.atomic
    def place_draft_orders(self, logged_in_user: User) -> List[Order]:
        cart: Cart = cart_service.fetch_user_cart_with_products_and_users(logged_in_user)
        if len(cart.cart_items.all()) == 0:
            raise Exception("error.empty.cart")
        distinct_suppliers = set()
        for cart_item in cart.cart_items.all():
            distinct_suppliers.add(cart_item.product.user)
        order_ids = []
        for supplier in distinct_suppliers:
            items = []
            new_order = self.place_order(logged_in_user, supplier)
            order_ids.append(new_order.id)
            filtered_by_supplier = filter(lambda ci: ci.product.user.id == supplier.id, cart.cart_items.all())
            for cart_item in filtered_by_supplier:
                order_item = order_repo.initialize_order_item(product_id=cart_item.product_id,
                                                              order_id=new_order.id,
                                                              product_name=cart_item.product.title,
                                                              sku=cart_item.product.sku,
                                                              price=cart_item.unit_price,
                                                              quantity=cart_item.quantity,
                                                              total_price=cart_item.total_price)
                items.append(order_item)
            new_order.order_items.add(*items, bulk=False)
            new_order.recalculate_order_total_price()
            self.update_order(new_order)
        cart_service.clear_cart(logged_in_user)
        return self.find_orders_by_ids(order_ids)

    @transaction.atomic
    def post_order_comment(self, request: PostOrderComment, logged_in_user: User) -> Order:
        serialized_data = request.data
        data_dict = dict(serialized_data)
        logger.info(f'data_dict: {data_dict}')
        order_id = data_dict['order_id']
        comment = data_dict['comment']
        order: Order = self.find_order_by_id(order_id, False)
        comment_repo.create_order_comment(comment, order, logged_in_user)
        return order_repo.find_order_by_id_with_products(order_id, True)

    @transaction.atomic
    def change_order_status(self, uuid: str, status: str) -> None:
        order: Order = order_repo.find_order_by_uuid(uuid)
        order.status = status
        if Order.OrderStatus.SHIPPED.__eq__(status):
            order.is_shipped = True
            order.date_shipped = timezone.now()
        self.update_order(order)

    def change_order_status_to_buyer_rejected(self, uuid: str) -> None:
        status = Order.OrderStatus.BUYER_REJECTED
        self.change_order_status(uuid, status)

    def change_order_status_to_supplier_rejected(self, uuid: str) -> None:
        status = Order.OrderStatus.SUPPLIER_REJECTED
        self.change_order_status(uuid, status)

    def change_order_status_to_approved(self, uuid: str) -> None:
        status = Order.OrderStatus.APPROVED
        self.change_order_status(uuid, status)

    def change_order_status_to_shipped(self, uuid: str) -> None:
        status = Order.OrderStatus.SHIPPED
        self.change_order_status(uuid, status)

    def change_order_status_to_received(self, uuid: str) -> None:
        status = Order.OrderStatus.RECEIVED
        self.change_order_status(uuid, status)

    def find_users_orders(self, user: User) -> List[Order]:
        return order_repo.find_users_orders(user)

    def find_orders_by_ids(self, order_ids: List[int]) -> List[Order]:
        order = Order.objects.filter(pk__in=order_ids)
        return order

    def find_order_ids_with_is_shipped(self):
        return order_repo.find_order_ids_with_is_shipped()

    def find_users_order_number(self, user: User) -> int:
        return order_repo.find_users_order_number(user)

    def find_users_largest_order(self, user: User) -> float:
        return order_repo.find_users_largest_order(user)

    def find_users_sum_order_price(self, user: User) -> float:
        return order_repo.find_users_sum_order_price(user)

    def find_total_sales_per_user(self) -> float:
        return order_repo.find_total_sales_per_user()

    def find_recendly_shipped_orders_by_supplier(self, user: User) -> List[Order]:
        return order_repo.find_recendly_shipped_orders_by_supplier(user)

    def find_received_orders_by_supplier(self, user: User) -> List[Order]:
        return order_repo.find_received_orders_by_supplier(user)

    def place_order(self, buyer, supplier) -> Order:
        return order_repo.place_order(buyer, supplier)

    def update_order(self, order: Order) -> Order:
        return order_repo.update_order(order)

    def find_order_by_uuid(self, uuid: str) -> Order:
        return order_repo.find_order_by_uuid_with_products(uuid, True)

    def find_order_by_id(self, order_id: int, fetch_items: bool) -> Order:
        return order_repo.find_order_by_id(order_id, fetch_items)

    def find_order_item_by_uuid(self, uuid: str) -> OrderItem:
        return order_repo.find_order_item_by_uuid(uuid)

    def find_order_item_by_id(self, order_item_id: int) -> OrderItem:
        return order_repo.find_order_item_by_id(order_item_id)

    def find_orders_by_requested_status(self, requested_status: str) -> List[Order]:
        return order_repo.find_orders_by_requested_status(requested_status)

    def update_order_item(self, order_item: OrderItem) -> OrderItem:
        return order_repo.update_order_item(order_item)

    def search_order_items(self, query: str, user: User = None) -> List[OrderItem]:
        return order_repo.search_order_items(query, user)
