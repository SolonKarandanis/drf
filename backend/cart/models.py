from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def create_cart(self, user):
        cart = self.create(user=user)
        return cart


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = CartManager()
