from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, QuerySet, Manager, Model, SET_NULL, ForeignKey, CharField, TextField, \
    FloatField, BooleanField, IntegerField, UUIDField, Index, SlugField, GeneratedField, PROTECT, ManyToManyField, \
    CASCADE
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.search import SearchVector, SearchVectorField
import uuid

# Create your models here.
User = settings.AUTH_USER_MODEL


class Category(Model):
    name = CharField(max_length=100)
    slug = SlugField(null=True)
    is_active = BooleanField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class Brand(Model):
    name = CharField(max_length=100)


class Attribute(Model):
    name = CharField(max_length=120, default=None)
    type = CharField(max_length=120, default=None)

    def __str__(self):
        return f"<Attribute name:{self.name} type:{self.type}>"


class AttributeOptions(Model):
    attribute = ForeignKey(Attribute, on_delete=CASCADE, related_name='attribute_options', null=True)
    option_name = CharField(max_length=120, default=None)

    def __str__(self):
        return f"<AttributeOptions option_name:{self.option_name} >"


class ProductQuerySet(QuerySet):
    def by_uuid(self, uuid: str):
        try:
            return self.get(uuid=uuid)
        except ObjectDoesNotExist:
            return None

    def is_public(self):
        return self.filter(public=True)

    def with_owner(self):
        return self.select_related('user')

    def with_comments(self):
        return self.prefetch_related('comments')

    def with_images(self):
        return self.prefetch_related('images')

    def owned_by(self, user):
        return self.filter(user=user)

    def inventory_number(self):
        return self.only('inventory')

    def product_skus(self):
        return self.values_list('sku', flat=True)

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs

    def fts_search(self, query, user=None):
        lookup = Q(title__search=query) | Q(content__search=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs


class ProductManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)


class Product(Model):
    user = ForeignKey(User, default=1, null=True, on_delete=SET_NULL)
    sku = CharField(max_length=120, default=None)
    title = CharField(max_length=120)
    content = TextField(blank=True, null=True)
    price = FloatField()
    public = BooleanField(db_default=True)
    inventory = IntegerField(blank=True, null=True)
    number_sold = IntegerField(blank=True, null=True)
    uuid = UUIDField(default=uuid.uuid4())
    comments = GenericRelation("comments.Comment", related_query_name='product')
    images = GenericRelation("images.Images", related_query_name='product')
    search = GeneratedField(
        db_persist=True,
        expression=SearchVector(
            "sku", "title", config="english"
        ),
        output_field=SearchVectorField(),
    )
    brand = ForeignKey(Brand, on_delete=PROTECT, db_default=1)
    category = ManyToManyField(Category, db_default=1)

    class Meta:
        ordering = ['sku']

        indexes = [
            Index(
                name='product_sku',
                fields=['sku'],
            ),
            Index(
                name='product_uuid',
                fields=['uuid'],
            ),
            Index(
                name='product_user_id',
                fields=['user_id'],
            )
        ]

    objects = ProductManager()

    def __str__(self):
        return f"<Product sku:{self.sku} title:{self.title}>"

    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.8)

    @classmethod
    def update_price(cls, product_id: int, price: float):
        product = cls.objects.get(pk=product_id)
        product = product.price = price
        product.save()
        return product

    @classmethod
    def create(cls):
        pass
