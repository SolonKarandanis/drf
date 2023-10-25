from django.db import models
from django.conf import settings

from products.models import Product

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def create_cart(self, user):
        cart = self.create(user=user)
        return cart


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    modification_alert = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_modified = models.DateTimeField(auto_now=True, null=False)
    objects = CartManager()

    def __repr__(self):
        return f"<Cart {self.id}>"


class CartItem(models.Model):
    modification_alert = models.BooleanField(default=False)
    quantity = models.IntegerField(blank=True, null=True)
    unit_price = models.FloatField()
    total_price = models.FloatField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __repr__(self):
        return f"<CartItem {self.id}>"
