from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, QuerySet, Manager, Model, SET_NULL, ForeignKey, CharField, TextField, \
    FloatField, BooleanField, IntegerField, UUIDField, Index, SlugField, GeneratedField, PROTECT, ManyToManyField, \
    CASCADE, TextChoices, DateTimeField, DecimalField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.search import SearchVector, SearchVectorField
import uuid
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

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

    def __str__(self):
        return f"<Brand name:{self.name}>"


class AttributeType(TextChoices):
    SINGLE = 'attribute.type.single',
    MULTIPLE = 'attribute.type.multiple',


class Attribute(Model):
    name = CharField(max_length=120, default=None)
    type = CharField(max_length=40, choices=AttributeType.choices, db_default=AttributeType.SINGLE)

    def __str__(self):
        return f"<Attribute name:{self.name} type:{self.type}>"


class AttributeOptionsQuerySet(QuerySet):
    def with_attribute(self):
        return self.select_related('attribute')

    def with_product_attribute_values(self):
        return self.prefetch_related('productattributevalues')


class AttributeOptionsManager(Manager):

    def get_queryset(self, *args, **kwargs):
        return AttributeOptionsQuerySet(self.model, using=self._db)


class AttributeOptions(Model):
    attribute = ForeignKey(Attribute, on_delete=CASCADE, related_name='attribute_options', null=True)
    option_name = CharField(max_length=120, default=None)

    objects = AttributeOptionsManager()

    class Meta:
        verbose_name_plural = "Attribute Options"
        db_table = 'products_attribute_options'

    def __str__(self):
        return f"<AttributeOptions attribute name: {self.attribute.name}, option_name:{self.option_name} >"


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
        qs = self.is_public()
        if query:
            lookup = Q(title__search=query) | Q(content__search=query) | Q(sku__search=query) | \
                     Q(fabric_details__search=query) | Q(care_instructions__search=query)
            qs = self.filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user)
            qs = (qs | qs2).distinct()
        return qs


class ProductManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)


class ProductPublishedStatus(TextChoices):
    PUBLISHED = 'product.status.published',
    SCHEDULED = 'product.status.scheduled',


class ProductAvailability(TextChoices):
    IN_STOCK = 'product.availability.in.stock',
    OUT_OF_STOCK = 'product.availability.out.of.stock',


class Product(Model):
    sku = CharField(max_length=120, default=None)
    title = CharField(max_length=120)
    content = TextField(blank=True, null=True)
    fabric_details = TextField(blank=True, null=True)
    care_instructions = TextField(blank=True, null=True)
    price = FloatField()
    public = BooleanField(db_default=True)
    inventory = IntegerField(blank=True, null=True)
    number_sold = IntegerField(blank=True, null=True)
    uuid = UUIDField(default=uuid.uuid4())
    search = GeneratedField(
        db_persist=True,
        expression=SearchVector(
            "sku", "title", "content", "fabric_details", "care_instructions", config="english"
        ),
        output_field=SearchVectorField(),
    )
    published_date = DateTimeField(auto_now_add=True, null=True)
    publish_status = CharField(max_length=40, choices=ProductPublishedStatus.choices,
                               db_default=ProductPublishedStatus.PUBLISHED)
    availability_status = CharField(max_length=40, choices=ProductAvailability.choices,
                                    db_default=ProductAvailability.IN_STOCK)

    comments = GenericRelation("comments.Comment", related_query_name='product')
    images = GenericRelation("images.Images", related_query_name='product')
    user = ForeignKey(User, default=1, null=True, on_delete=SET_NULL)
    brand = ForeignKey(Brand, on_delete=PROTECT, db_default=1)
    category = ManyToManyField(Category, db_default=1)
    attributes = ManyToManyField(Attribute, through="ProductAttributeValues")

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


class ProductAttributeValuesQuerySet(QuerySet):
    def with_attribute(self):
        return self.select_related('attribute')

    def with_attribute_option(self):
        return self.select_related('attribute_option')


class ProductAttributeValuesManager(Manager):

    def get_queryset(self, *args, **kwargs):
        return ProductAttributeValuesQuerySet(self.model, using=self._db)


class ProductAttributeValues(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    attribute = ForeignKey(Attribute, on_delete=CASCADE)
    attribute_option = ForeignKey(AttributeOptions, on_delete=CASCADE)
    attribute_value_method = CharField(max_length=120, default=None, null=True, blank=True)
    attribute_value = FloatField(null=True, blank=True)

    objects = ProductAttributeValuesManager()

    class Meta:
        verbose_name_plural = "Product Attribute Values"
        db_table = 'products_attribute_values'

    def __str__(self):
        return f"<ProductAttributeValues product:{self.product} attribute:{self.attribute}>"


class DiscountType(TextChoices):
    SINGLE = 'attribute.type.single',
    MULTIPLE = 'attribute.type.multiple',


class Discount(Model):
    name = CharField(max_length=255)
    type = CharField(max_length=40, choices=DiscountType.choices, db_default=DiscountType.SINGLE)
    description = TextField(blank=True)
    promo_reduction = IntegerField(default=0)
    is_active = BooleanField(default=False)
    is_schedule = BooleanField(default=False)
    promo_start = DateTimeField()
    promo_end = DateTimeField()

    def clean(self):
        if self.promo_start > self.promo_end:
            raise ValidationError(_("End data before the start date"))

    def __str__(self):
        return f"<Discount name:{self.name} type:{self.type}>"


class ProductsDiscount(Model):
    product_id = ForeignKey(
        Product,
        on_delete=PROTECT,
    )
    discount_id = ForeignKey(
        Discount,
        on_delete=CASCADE,
    )
    discount_price = DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )
    price_override = BooleanField(
        default=False,
    )

    class Meta:
        unique_together = (("product_id", "discount_id"),)
        verbose_name_plural = "Products Discounts"
        db_table = 'products_product_discount'
