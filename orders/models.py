import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Max, Sum, Manager, QuerySet, Model, DateTimeField, CharField, FloatField, TextField, \
    ForeignKey, BooleanField, CASCADE, UniqueConstraint, Index, IntegerField, PROTECT, Case, When, TextChoices, Count, \
    Value, UUIDField
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres import indexes, search as fts
import uuid
from products.models import Product

User = settings.AUTH_USER_MODEL
logger = logging.getLogger('django')


class OrderQuerySet(QuerySet):

    def by_uuid(self, uuid: str):
        try:
            return self.get(uuid=uuid)
        except ObjectDoesNotExist:
            return None

    def with_comments(self):
        return self.prefetch_related('comments')

    def with_order_items(self):
        return self.prefetch_related('order_items')

    def owned_by(self, user):
        return self.filter(buyer=user)

    def supplied_by(self, user):
        return self.filter(supplier=user)

    def order_ids_with_is_shipped(self):
        return self.values('id', 'is_shipped')

    def max_total_price(self):
        return self.aggregate(max=Max('total_price'))

    def sum_total_price(self):
        return self.aggregate(sum=Sum('total_price'))

    def total_sales(self):
        return self.values('user') \
            .annotate(total_sales=Sum('total_price')).values('user__id', 'user__name', 'total_price')

    def recently_shipped(self):
        recently_shipped = Q(is_shipped=True) & \
                           Q(date_shipped__gt=timezone.now() - timezone.timedelta(days=30))
        return self.filter(recently_shipped)

    def received(self):
        received = Order.OrderStatus.RECEIVED
        self.annotate(
            is_received=Case(
                When(status=received, then=True),
                default=False
            )
        ).filter(is_received=True)

    def by_status(self, requested_status: str):
        order_status = Order.OrderStatus
        return self.annotate(
            Case(
                When(Q(status=order_status.BUYER_REJECTED) |
                     Q(status=order_status.SUPPLIER_REJECTED), then=Value("rejected")),
                When(Q(status=order_status.APPROVED) | Q(status=order_status.SHIPPED) |
                     Q(status=order_status.RECEIVED), then=Value("successful")),
                default=Value("draft")
            )
        ).filter(order_status=requested_status)


class OrderManager(Manager):
    def create_order(self, buyer, supplier):
        draft_status = Order.OrderStatus.DRAFT
        order = self.create(buyer=buyer, supplier=supplier, total_price=0, status=draft_status)
        order.save()
        return order

    def update_order(self, order):
        order = order.save()
        return order

    def get_queryset(self, *args, **kwargs):
        return OrderQuerySet(self.model, using=self._db)


# Create your models here.
class Order(Model):
    class OrderStatus(TextChoices):
        DRAFT = 'purchase.order.draft',
        BUYER_REJECTED = 'purchase.order.buyer.rejected',
        SUPPLIER_REJECTED = 'purchase.order.supplier.rejected',
        APPROVED = 'purchase.order.approved',
        SHIPPED = 'purchase.order.shipped',
        RECEIVED = 'purchase.order.received'

    date_created = DateTimeField(auto_now_add=True, null=False)
    status = CharField(max_length=40, choices=OrderStatus.choices)
    total_price = FloatField()
    buyer = ForeignKey(User, on_delete=CASCADE, related_name='buyer')
    is_shipped = BooleanField(default=False)
    date_shipped = DateTimeField(null=True)
    supplier = ForeignKey(User, on_delete=CASCADE, related_name='supplier')
    uuid = UUIDField(default=uuid.uuid4())
    comments = GenericRelation("comments.Comment", related_query_name='order')

    objects = OrderManager()

    class Meta:
        ordering = ['-date_created']

        constraints = [
            UniqueConstraint(
                name='limit_pending_orders',
                fields=['buyer_id', 'is_shipped'],
                condition=Q(is_shipped=False)
            )
        ]

        indexes = [
            Index(
                name='unshipped_orders',
                fields=['id'],
                condition=Q(is_shipped=False)
            ),
            Index(
                name='order_buyer_id',
                fields=['buyer_id'],
                condition=Q(is_shipped=False)
            ),
            Index(
                name='order_supplier_id',
                fields=['supplier_id'],
                condition=Q(is_shipped=False)
            )
        ]

    def __repr__(self):
        return f"<Order {self.id}>"

    def recalculate_order_total_price(self) -> None:
        self.total_price = sum(oi.total_price for oi in self.order_items.all())


# notify supplier for new order
@receiver(pre_save, sender=Order, dispatch_uid='order_created')
def order_created_handler(sender, instance, **kwargs):
    supplier_id = instance.supplier.id


# notify buyer and supplier of order status
@receiver(pre_save, sender=Order, dispatch_uid='order_status_changed')
def order_status_changed_handler(sender, instance, **kwargs):
    supplier_id = instance.supplier.id


vector = fts.SearchVector("product_name", "sku", "manufacturer", config="english")


class OrderItemQuerySet(QuerySet):

    def search(self, query, user=None):
        lookup = Q(sku__icontains=query) | Q(product_name__icontains=query) | Q(manufacturer__icontains=query)
        qs = self.filter(lookup)
        if user is not None:
            qs2 = self.filter(order__user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs

    def fts_search(self, query, user=None):
        # Django 5
        # OrderItem.objects.filter(search="meanings")
        s_query = fts.SearchQuery(query)
        qs = self.annotate(search=vector).filter(search=s_query)
        if user is not None:
            qs.filter(order__buyer=user)
        return qs

    def is_popular(self):
        self.annotate(number_of_sales=Count('product'))
        return self.annotate(
            is_popular=Case(
                When(number_of_sales__gt=9, then=True),
                default=False
            )
        ).filter(is_popular=True)

    def with_product(self):
        return self.select_related('product')


class OrderItemManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return OrderItemQuerySet(self.model, using=self._db)

    def update_item(self, order_item):
        order_item = order_item.save()
        return order_item

    def create_order_item(self, product_id: int, order_id: int, product_name: str, sku: str,
                          price: float, quantity: float, total_price: float):
        order_item = self.create(product_id=product_id, order_id=order_id, product_name=product_name, sku=sku,
                                 price=price, quantity=quantity, total_price=total_price, manufacturer="",
                                 uuid=uuid.uuid4())
        return order_item


class OrderItem(Model):
    product_name = CharField(max_length=255)
    sku = CharField(max_length=120, default=None)
    manufacturer = CharField(max_length=255, default=None)
    start_date = DateTimeField(auto_now_add=True, null=False)
    end_date = DateTimeField(null=True)
    status = CharField(max_length=40)
    price = FloatField()
    quantity = IntegerField(blank=True, null=True)
    total_price = FloatField()
    order = ForeignKey(Order, on_delete=CASCADE, related_name='order_items')
    product = ForeignKey(Product, on_delete=PROTECT)
    uuid = UUIDField(default=uuid.uuid4())
    #  django 5!!!!
    # search = GeneratedField(
    #     db_persist=True,
    #     expression=SearchVector(
    #         "product_name","manufacturer", config="english"
    #     ),
    #     output_field=SearchVectorField(),
    # )

    objects = OrderItemManager()

    class Meta:
        indexes = [
            indexes.GinIndex(vector, name="s_order_item_product_name_idx")
        ]

    def __repr__(self):
        return f"<OrderItem {self.id}>"
