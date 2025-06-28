from django.db.models import Model, ForeignKey, PROTECT, SET_NULL, DateTimeField, UUIDField, QuerySet, Manager, \
    JSONField, Index
from django.conf import settings
import uuid
from products.models import Product

User = settings.AUTH_USER_MODEL


class WishListItemQuerySet(QuerySet):
    def with_product(self):
        return self.select_related('product')

    def owned_by(self, user):
        return self.get(user=user)


class WishListItemManager(Manager):

    def create_wish_list_item(self, product: Product, user: User, attributes: str):
        wishlist_item = self.create(product=product, user=user, attributes=attributes, uuid=uuid.uuid4())
        return wishlist_item

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

    class Meta:
        indexes = [
            Index(
                name='wishlist_item_user_id',
                fields=['user_id'],
            )
        ]

    def __repr__(self):
        return f"<WishListItem {self.id}>"
