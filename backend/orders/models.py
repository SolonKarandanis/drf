from django.db import models
from django.conf import settings

from products.models import Product

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
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __repr__(self):
        return f"<OrderItem {self.id}>"
