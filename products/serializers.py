import logging

from rest_framework import serializers
from django.core.paginator import Paginator
from .models import Product
from .validators import unique_product_title, validate_sku, product_exists
from auth.serializers import UserPublicSerializer
from comments.serializers import CommentSerializer

logger = logging.getLogger('django')

AVAILABILITY_STATUS_CHOICES = [
    "product.availability.in.stock",
    "product.availability.out.of.stock",
]

PUBLISH_STATUS_CHOICES = [
    "product.status.published",
    "product.status.scheduled",
]


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[unique_product_title])
    owner = UserPublicSerializer(source='user', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    fabricDetails = serializers.CharField(source='fabric_details', read_only=True)
    careInstructions = serializers.CharField(source='care_instructions', read_only=True)
    publishStatus = serializers.ChoiceField(source='publish_status', read_only=True, choices=PUBLISH_STATUS_CHOICES)
    availabilityStatus = serializers.ChoiceField(source='availability_status', read_only=True,
                                                 choices=AVAILABILITY_STATUS_CHOICES)
    salePrice = serializers.FloatField(source='sale_price', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'title',
            'content',
            'fabricDetails',
            'careInstructions',
            'publishStatus',
            'availabilityStatus',
            'owner',
            'price',
            'inventory',
            'salePrice',
            'uuid',
            'comments'
        ]


class ProductListSerializer(serializers.ModelSerializer):
    fabricDetails = serializers.CharField(source='fabric_details', read_only=True)
    careInstructions = serializers.CharField(source='care_instructions', read_only=True)
    publishStatus = serializers.CharField(source='publish_status', read_only=True)
    availabilityStatus = serializers.CharField(source='availability_status', read_only=True)
    salePrice = serializers.FloatField(source='sale_price', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'title',
            'content',
            'fabricDetails',
            'careInstructions',
            'publishStatus',
            'availabilityStatus',
            'price',
            'inventory',
            'salePrice',
            'uuid'
        ]


class PageNotAnInteger:
    pass


class EmptyPage:
    pass


class PaginatedProductListSerializer:
    """
    Serializes page objects of product querysets.
    """

    def __init__(self, data, request):
        page = request.GET.get('page', 1)
        size = request.GET.get('size', 10)
        logger.info(f'page: {page}')
        logger.info(f'size: {size}')
        paginator = Paginator(data, size)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        count = paginator.count

        previous = None if not data.has_previous() else data.previous_page_number()
        next = None if not data.has_next() else data.next_page_number()
        serializer = ProductListSerializer(data, many=True)
        self.page_data = {'count': count, 'previous': previous, 'next': next, 'data': serializer.data}


class CreateProductSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(validators=[validate_sku])
    title = serializers.CharField(validators=[unique_product_title])
    fabricDetails = serializers.CharField(source='fabric_details', read_only=True)
    careInstructions = serializers.CharField(source='care_instructions', read_only=True)
    publishStatus = serializers.CharField(source='publish_status', read_only=True)
    availabilityStatus = serializers.CharField(source='availability_status', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'title',
            'content',
            'fabricDetails',
            'careInstructions',
            'price',
            'inventory',
            'publishStatus',
            'availabilityStatus',
        ]

    # def save(self):
    #     user = self.context.get("logged_in_user")
    #     sku = self.validated_data['sku']
    #     title = self.validated_data['title']
    #     content = self.validated_data['content']
    #     price = self.validated_data['price']
    #     inventory = self.validated_data['inventory']
    #     new_product = Product(sku=sku, user=user, title=title, content=content, price=price, inventory=inventory)
    #     new_product.save()
    #     return new_product


class PostProductComment(serializers.Serializer):
    productId = serializers.IntegerField(source='product_id', validators=[product_exists])
    comment = serializers.CharField()

    class Meta:
        fields = [
            'productId',
            'comment',
        ]

    def __repr__(self):
        return f"<PostProductComment ProductId:{self.product_id},  Comment:{self.comment}>"


class ProductSearchRequestSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
    category_id = serializers.IntegerField(required=False)
    brand_id = serializers.IntegerField(required=False)
    size_id = serializers.IntegerField(required=False)

    class Meta:
        fields = [
            'query',
        ]

    def __repr__(self):
        return f"<ProductSearchRequest query:{self.query},Category:{self.category_id}, Brand:{self.brand_id}, Size:{self.size_id}>"


class CategoriesWithTotalsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    totalProducts = serializers.IntegerField(source='total_products', read_only=True)

    class Meta:
        fields = [
            'id',
            'name',
            'totalProducts',
        ]


class BrandsWithTotalsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    totalProducts = serializers.IntegerField(source='total_products', read_only=True)

    class Meta:
        fields = [
            'id',
            'name',
            'totalProducts',
        ]


class SizesWithTotalsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    totalProducts = serializers.IntegerField(source='total_products', read_only=True)

    class Meta:
        fields = [
            'id',
            'name',
            'totalProducts',
        ]


class DiscountsWithTotalsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    totalProducts = serializers.IntegerField(source='total_products', read_only=True)

    class Meta:
        fields = [
            'id',
            'name',
            'totalProducts',
        ]
