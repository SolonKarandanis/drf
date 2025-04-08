from django.db.models import Model, ForeignKey, PROTECT, SET_NULL, DateTimeField, UUIDField, QuerySet, Manager, \
    JSONField
from django.conf import settings
import uuid
from products.models import Product

User = settings.AUTH_USER_MODEL


class WishListItemQuerySet(QuerySet):
    def with_product(self):
        return self.select_related('product')


class WishListItemManager(Manager):

    # def create_wish_list_item(self, quantity: int, unit_price: float, total_price: float, product_id: int, cart: Cart,
    #                      attributes: str):
    #     cart_item = self.create(quantity=quantity, unit_price=unit_price, total_price=total_price,
    #                             attributes=attributes, product_id=product_id, cart=cart, uuid=uuid.uuid4())
    #     return cart_item
    #
    # def update_cart_item(self, cart_item):
    #     cart_item = cart_item.save()
    #     return cart_item

    def get_queryset(self, *args, **kwargs):
        return WishListItemQuerySet(self.model, using=self._db)


class WishListItem(Model):
    product = ForeignKey(Product, on_delete=PROTECT)
    user = ForeignKey(User, default=1, null=True, on_delete=SET_NULL)
    date_created = DateTimeField(auto_now_add=True, null=False)
    date_modified = DateTimeField(auto_now=True, null=False)
    uuid = UUIDField(default=uuid.uuid4())
    attributes = JSONField(null=True)

    @property
    def _attributes(self):
        return self.attributes

    objects = WishListItemManager()

    def __repr__(self):
        return f"<WishListItem {self.id}>"
