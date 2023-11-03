from django.db import models
from django.conf import settings

from products.models import Product

User = settings.AUTH_USER_MODEL


class CartQuerySet(models.QuerySet):
    def owned_by(self, user):
        return self.filter(user=user)

    def with_cart_items(self):
        return self.prefetch_related('cart_items')


class CartManager(models.Manager):
    def create_cart(self, user):
        cart = self.create(user=user)
        return cart

    def get_queryset(self, *args, **kwargs):
        return CartQuerySet(self.model, using=self._db)


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    modification_alert = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_modified = models.DateTimeField(auto_now=True, null=False)
    objects = CartManager()

    def add_item_to_cart(self, products_id: int, quantity: int, price: float) -> None:
        existing_cart_item = next(filter(lambda ci: ci.products_id == products_id, self.cart_items), None)
        if existing_cart_item is None:
            cart_item = CartItem(quantity=quantity,
                                 modification_alert=False,
                                 unit_price=price,
                                 total_price=quantity * price,
                                 products_id=products_id)
            self.cart_items.append(cart_item)
        else:
            new_quantity = existing_cart_item.quantity + quantity
            existing_cart_item.quantity = new_quantity
            existing_cart_item.total_price = new_quantity * price

        self.update_cart_total_price()

    def update_item_quantity(self, cart_item_id: int, quantity: int) -> None:
        existing_cart_item = next(filter(lambda ci: ci.id == cart_item_id, self.cart_items), None)
        if existing_cart_item is not None:
            existing_cart_item.quantity = quantity
            existing_cart_item.total_price = quantity * existing_cart_item.unit_price
            self.update_cart_total_price()

    def remove_from_cart(self, cart_item) -> None:
        self.cart_items.remove(cart_item)
        self.update_cart_total_price()

    def clear_cart(self) -> None:
        self.cart_items.clear()
        self.update_cart_total_price()

    def update_cart_total_price(self) -> None:
        self.total_price = sum(ci.total_price for ci in self.cart_items)

    def __repr__(self):
        return f"<Cart {self.id}>"


class CartItem(models.Model):
    modification_alert = models.BooleanField(default=False)
    quantity = models.IntegerField(blank=True, null=True)
    unit_price = models.FloatField()
    total_price = models.FloatField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __repr__(self):
        return f"<CartItem {self.id}>"
