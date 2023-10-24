from django.db import models
from django.db.models import Q
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL


class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def with_owner(self):
        # prefetch_related()
        return self.select_related('user')

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs


class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)


class Product(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    public = models.BooleanField(default=True)
    inventory = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['title']

    objects = ProductManager()

    def __str__(self):
        return f"{self.title}"

    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.8)

    @classmethod
    def update_price(cls, product_id, price):
        product = cls.objects.get(pk=product_id)
        product = product.price = price
        product.save()
        return product

    @classmethod
    def create(cls):
        pass
