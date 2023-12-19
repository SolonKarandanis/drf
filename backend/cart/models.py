import logging
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db.models import QuerySet, DateTimeField, Manager, Model, OneToOneField, FloatField, BooleanField, CASCADE, \
    UniqueConstraint, Index, IntegerField, ForeignKey, PROTECT, UUIDField, Prefetch
from django.conf import settings
import uuid

from products.models import Product

User = settings.AUTH_USER_MODEL
key_prefix = settings.CACHES.get('default').get('KEY_PREFIX')
logger = logging.getLogger('django')


class CartQuerySet(QuerySet):
    def by_uuid(self, uuid: str):
        try:
            return self.get(uuid=uuid)
        except ObjectDoesNotExist:
            return None

    def owned_by(self, user):
        try:
            cart = self.get(user=user)
        except ObjectDoesNotExist:
            cart = self.create(user=user, total_price=0)
        return cart

    def with_cart_items(self):
        cart_items_prefect = Prefetch('cart_items', queryset=CartItem.objects.select_related('product'))
        return self.prefetch_related(cart_items_prefect)

    def update(self, **kwargs):
        user = kwargs.get("user")
        user_id = user.id
        cache_key = f'{key_prefix}:1:cart-{user_id}'
        cache.delete(cache_key)
        super(CartQuerySet, self).update(**kwargs)


class CartManager(Manager):
    def create_cart(self, user):
        cart = self.create(user=user, total_price=0)
        return cart

    def update_cart(self, cart):
        cart = cart.save()
        return cart

    def get_queryset(self, *args, **kwargs):
        return CartQuerySet(self.model, using=self._db)


# Create your models here.
class Cart(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    total_price = FloatField()
    modification_alert = BooleanField(default=False)
    date_created = DateTimeField(auto_now_add=True, null=False)
    date_modified = DateTimeField(auto_now=True, null=False)
    uuid = UUIDField(default=uuid.uuid4())
    objects = CartManager()

    class Meta:
        constraints = [
            UniqueConstraint(
                name='one_cart_per_user',
                fields=['id', 'user']
            )
        ]

        indexes = [
            Index(
                name='cart_user_id',
                fields=['user_id'],
            )
        ]

    def recalculate_cart_total_price(self) -> None:
        self.total_price = sum(ci.total_price for ci in self.cart_items.all())

    def __repr__(self):
        return f"<Cart id:{self.id} >"


class CartItemQuerySet(QuerySet):
    def with_product(self):
        return self.select_related('product')


class CartItemManager(Manager):

    def create_cart_item(self, quantity: int, unit_price: float, total_price: float, product_id: int, cart: Cart):
        cart_item = self.create(quantity=quantity, unit_price=unit_price, total_price=total_price,
                                product_id=product_id, cart=cart, uuid=uuid.uuid4())
        return cart_item

    def update_cart_item(self, cart_item):
        cart_item = cart_item.save()
        return cart_item

    def get_queryset(self, *args, **kwargs):
        return CartItemQuerySet(self.model, using=self._db)


class CartItem(Model):
    modification_alert = BooleanField(default=False)
    quantity = IntegerField(blank=True, null=True)
    unit_price = FloatField()
    total_price = FloatField()
    cart = ForeignKey(Cart, on_delete=CASCADE, related_name='cart_items', null=True)
    product = ForeignKey(Product, on_delete=PROTECT)
    uuid = UUIDField(default=uuid.uuid4())

    objects = CartItemManager()

    def __repr__(self):
        return f"<CartItem {self.id}>"


@receiver(post_delete, sender=CartItem, dispatch_uid='cart_item_deleted')
def cart_item_post_delete_handler(sender, instance, **kwargs):
    user_id = instance.cart.user.id
    cache_key = f'{key_prefix}:1:cart-{user_id}'
    cache.delete(cache_key)


@receiver(post_save, sender=CartItem, dispatch_uid='cart_item_updated')
def cart_item_post_save_handler(sender, instance, **kwargs):
    user_id = instance.cart.user.id
    cache_key = f'{key_prefix}:1:cart-{user_id}'
    cache.delete(cache_key)


@receiver(post_delete, sender=Cart, dispatch_uid='cart_deleted')
def cart__post_delete_handler(sender, instance, **kwargs):
    user_id = instance.user.id
    cache_key = f'{key_prefix}:1:cart-{user_id}'
    cache.delete(cache_key)


@receiver(post_save, sender=Cart, dispatch_uid='cart_updated')
def cart_post_save_handler(sender, instance, **kwargs):
    user_id = instance.user.id
    cache_key = f'{key_prefix}:1:cart-{user_id}'
    cache.delete(cache_key)
