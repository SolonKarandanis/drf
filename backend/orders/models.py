from typing import List

from django.db import models, transaction
from django.conf import settings
from django.utils import timezone

from products.models import Product
from cart.models import CartItem

User = settings.AUTH_USER_MODEL


class OrderQuerySet(models.QuerySet):
    def with_order_items(self):
        return self.prefetch_related('order_items')

    def owned_by(self, user):
        return self.filter(user=user)


class OrderManager(models.Manager):
    def create_order(self, user):
        order = self.create(user=user, total_price=0)
        return order

    def update_order(self):
        order = self.save()
        return order

    def get_queryset(self, *args, **kwargs):
        return OrderQuerySet(self.model, using=self._db)


# Create your models here.
class Order(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    status = models.CharField(max_length=40)
    total_price = models.FloatField()
    comments = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_shipped = models.BooleanField(default=False)
    objects = OrderManager()

    class Meta:
        ordering = ['-date_created']

        constraints = [
            models.UniqueConstraint(
                name='limit_pending_orders',
                fields=['user_id', 'is_shipped'],
                condition=models.Q(is_shipped=False)
            )
        ]

        indexes = [
            models.Index(
                name='unshipped_orders',
                fields=['id'],
                condition=models.Q(is_shipped=False)
            ),
            models.Index(
                name='order_user_id',
                fields=['user_id']
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


class OrderItem(models.Model):
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=120, default=None)
    manufacturer = models.CharField(max_length=255, default=None)
    start_date = models.DateTimeField(auto_now_add=True, null=False)
    end_date = models.DateTimeField(null=False)
    status = models.CharField(max_length=40)
    price = models.FloatField()
    quantity = models.IntegerField(blank=True, null=True)
    total_price = models.FloatField()
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __repr__(self):
        return f"<OrderItem {self.id}>"
