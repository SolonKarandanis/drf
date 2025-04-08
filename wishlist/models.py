from django.db.models import Model, ForeignKey, PROTECT, SET_NULL, DateTimeField, UUIDField
from django.conf import settings
import uuid
from products.models import Product

User = settings.AUTH_USER_MODEL


# Create your models here.
class WishListItem(Model):
    product = ForeignKey(Product, on_delete=PROTECT)
    user = ForeignKey(User, default=1, null=True, on_delete=SET_NULL)
    date_created = DateTimeField(auto_now_add=True, null=False)
    date_modified = DateTimeField(auto_now=True, null=False)
    uuid = UUIDField(default=uuid.uuid4())
