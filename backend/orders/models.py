from typing import List

from django.db import transaction
from django.db.models import Q, Max, Sum, Manager, QuerySet, Model, DateTimeField, CharField, FloatField, TextField, \
    ForeignKey, BooleanField, CASCADE, UniqueConstraint, Index, IntegerField, PROTECT, Case, When, TextChoices
from django.conf import settings
from django.utils import timezone

from products.models import Product
from cart.models import CartItem

User = settings.AUTH_USER_MODEL


class OrderQuerySet(QuerySet):
    def with_order_items(self):
        return self.prefetch_related('order_items')

    def owned_by(self, user):
        return self.filter(user=user)

    def order_ids_with_is_shipped(self):
        return self.values('id', 'is_shipped')

    def max_total_price(self):
        return self.aggregate(max=Max('total_price'))

    def sum_total_price(self):
        return self.aggregate(sum=Sum('total_price'))

    def total_sales(self):
        return self.values('user') \
            .annotate(total_sales=Sum('total_price')).values('user__id', 'user__name', 'total_price')

    def recently_shipped(self):
        recently_shipped = Q(date_shipped__gt=timezone.now() - timezone.timedelta(days=30))
        return self.filter(recently_shipped)

    def shipped(self, shipped: bool):
        self.annotate(
            is_shipped=Case(
                When(is_shipped)
            )
        )


class OrderManager(Manager):
    def create_order(self, user):
        order = self.create(user=user, total_price=0)
        return order

    def update_order(self):
        order = self.save()
        return order

    def get_queryset(self, *args, **kwargs):
        return OrderQuerySet(self.model, using=self._db)


# Create your models here.
class Order(Model):
    class OrderStatus(TextChoices):
        DRAFT = 'purchase.order.draft',
        BUYER_REJECTED = 'purchase.order.buyer.rejected',
        SUPPLIER_REJECTED = 'purchase.order.supplier.rejected',
        APPROVED = 'purchase.order.approved',
        SHIPPED = 'purchase.order.shipped',
        RECEIVED = 'purchase.order.received'

    date_created = DateTimeField(auto_now_add=True, null=False)
    status = CharField(max_length=40, choices=OrderStatus.choices)
    total_price = FloatField()
    comments = TextField(blank=True, null=True)
    buyer = ForeignKey(User, on_delete=CASCADE, related_name='buyer')
    is_shipped = BooleanField(default=False)
    date_shipped = DateTimeField(null=True)
    supplier = ForeignKey(User, on_delete=CASCADE, related_name='supplier')
    objects = OrderManager()

    class Meta:
        ordering = ['-date_created']

        constraints = [
            UniqueConstraint(
                name='limit_pending_orders',
                fields=['buyer_id', 'is_shipped'],
                condition=Q(is_shipped=False)
            )
        ]

        indexes = [
            Index(
                name='unshipped_orders',
                fields=['id'],
                condition=Q(is_shipped=False)
            ),
            Index(
                name='order_buyer_id',
                fields=['buyer_id'],
                condition=Q(is_shipped=False)
            ),
            Index(
                name='order_supplier_id',
                fields=['supplier'],
                condition=Q(is_shipped=False)
            )
        ]

    def __repr__(self):
        return f"<Order {self.id}>"

    @transaction.atomic
    def add_order_items(self, cart_items: List[CartItem]) -> None:
        items = []
        for cart_item in cart_items:
            order_item = OrderItem(product_id=cart_item.products_id,
                                   product_name=cart_item.product.name,
                                   sku=cart_item.product.sku,
                                   manufacturer=cart_item.product.supplier,
                                   start_date=timezone.now(),
                                   status=self.status,
                                   price=cart_item.unit_price,
                                   quantity=cart_item.quantity,
                                   total_price=cart_item.total_price)
            items.append(order_item)
        self.order_items.append(*items, bulk=False)
        self.update_order_total_price()

    def update_order_total_price(self) -> None:
        self.total_price = sum(oi.total_price for oi in self.order_items.all())
        self.save()


class OrderItemQuerySet(QuerySet):

    def search_order_items(self, query, user=None):
        lookup = Q(sku__icontains=query) | Q(product_name__icontains=query) | Q(manufacturer__icontains=query)
        qs = self.filter(lookup)
        if user is not None:
            qs2 = self.filter(order__user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs


class OrderItemManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return OrderItemQuerySet(self.model, using=self._db)


class OrderItem(Model):
    product_name = CharField(max_length=255)
    sku = CharField(max_length=120, default=None)
    manufacturer = CharField(max_length=255, default=None)
    start_date = DateTimeField(auto_now_add=True, null=False)
    end_date = DateTimeField(null=False)
    status = CharField(max_length=40)
    price = FloatField()
    quantity = IntegerField(blank=True, null=True)
    total_price = FloatField()
    order = ForeignKey(Order, on_delete=CASCADE, related_name='order_items')
    product = ForeignKey(Product, on_delete=PROTECT)

    def __repr__(self):
        return f"<OrderItem {self.id}>"
