from typing import List

from django.db import models
from django.conf import settings
from django.utils import timezone

from products.models import Product
from cart.models import CartItem

User = settings.AUTH_USER_MODEL


# Create your models here.
class Order(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    status = models.CharField(max_length=40)
    total_price = models.FloatField()
    comments = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_created']

    def __repr__(self):
        return f"<Order {self.id}>"

    def add_order_items(self, cart_items: List[CartItem]) -> None:
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
            self.order_items.append(order_item)


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
