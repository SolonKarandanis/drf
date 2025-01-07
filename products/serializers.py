import logging

from rest_framework import serializers
from django.core.paginator import Paginator

from cfehome.serializers import PagingSerializer
from images.serializers import ImagesSerializer
from .models import Product, Brand, Category, AttributeOptions, ProductAttributeValues
from .validators import unique_product_title, validate_sku, product_exists
from auth.serializers import UserPublicSerializer
from comments.serializers import CommentSerializer

logger = logging.getLogger('django')

AVAILABILITY_STATUS_CHOICES = [
    "product.availability.in.stock",
    "product.availability.out.of.stock",
]

AVAILABILITY_STATUS_LABEL_OPTIONS = {
    "product.availability.in.stock": "In Stock",
    "product.availability.out.of.stock": "Out of Stock",
}

PUBLISH_STATUS_CHOICES = [
    "product.status.published",
    "product.status.scheduled",
]

PUBLISH_STATUS_LABEL_OPTIONS = {
    "product.status.published": "Published",
    "product.status.scheduled": "Scheduled",
}


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug'
        ]


class AttributeOptionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='option_name', read_only=True)

    class Meta:
        model = AttributeOptions
        fields = [
            'id',
            'name',
        ]


class ProductAttributeValuesSerializer(serializers.ModelSerializer):
    productId = serializers.IntegerField(source='product__id', read_only=True)
    attributeId = serializers.IntegerField(source='attribute__id', read_only=True)
    attributeOptionId = serializers.IntegerField(source='attribute_option__id', read_only=True)

    class Meta:
        model = ProductAttributeValues
        fields = [
            'id',
            'productId',
            'attributeId',
            'attributeOptionId',
        ]


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[unique_product_title])
    owner = UserPublicSerializer(source='user', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    fabricDetails = serializers.CharField(source='fabric_details', read_only=True)
    careInstructions = serializers.CharField(source='care_instructions', read_only=True)
    publishStatus = serializers.ChoiceField(source='publish_status', read_only=True, choices=PUBLISH_STATUS_CHOICES)
    publishStatusLabel = serializers.SerializerMethodField('_get_publish_status_label')
    availabilityStatus = serializers.ChoiceField(source='availability_status', read_only=True,
                                                 choices=AVAILABILITY_STATUS_CHOICES)
    availabilityStatusLabel = serializers.SerializerMethodField('_get_availability_status_label')
    salePrice = serializers.FloatField(source='sale_price', read_only=True)
    averageRating = serializers.FloatField(source='average_rating', read_only=True)
    numberOfRatings = serializers.IntegerField(source='number_of_ratings', read_only=True)
    brand = BrandSerializer(read_only=True)
    categories = CategorySerializer(source='category', many=True, read_only=True)

    def _get_availability_status_label(self, product_object) -> str:
        availability_status = getattr(product_object, 'availability_status')
        return AVAILABILITY_STATUS_LABEL_OPTIONS[availability_status]

    def _get_publish_status_label(self, product_object) -> str:
        publish_status = getattr(product_object, 'publish_status')
        return PUBLISH_STATUS_LABEL_OPTIONS[publish_status]

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
            'publishStatusLabel',
            'availabilityStatus',
            'availabilityStatusLabel',
            'owner',
            'brand',
            'categories',
            'price',
            'inventory',
            'salePrice',
            'averageRating',
            'numberOfRatings',
            'uuid',
            'comments',
        ]


class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='product.id', read_only=True)
    sku = serializers.CharField(source='product.sku', read_only=True)
    title = serializers.CharField(source='product.title', read_only=True)
    content = serializers.CharField(source='product.content', read_only=True)
    fabricDetails = serializers.CharField(source='product.fabric_details', read_only=True)
    careInstructions = serializers.CharField(source='product.care_instructions', read_only=True)
    publishStatus = serializers.CharField(source='product.publish_status', read_only=True)
    availabilityStatus = serializers.CharField(source='product.availability_status', read_only=True)
    price = serializers.FloatField(source='product.price', read_only=True)
    inventory = serializers.IntegerField(source='product.inventory', read_only=True)
    salePrice = serializers.FloatField(source='product.sale_price', read_only=True)
    uuid = serializers.CharField(source='product.uuid', read_only=True)
    previewImage = ImagesSerializer(source='preview_image', read_only=True)
    averageRating = serializers.FloatField(source='product.average_rating', read_only=True)

    class Meta:
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
            'averageRating',
            'previewImage',
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


class PaginatedPOSTProductListSerializer:
    """
    Serializes page objects of product querysets.
    """

    def __init__(self, data, paging):
        limit = paging["limit"]
        page = paging["page"]
        logger.info(f'page: {page}')
        logger.info(f'size: {limit}')
        paginator = Paginator(data, limit)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        count = paginator.count
        pages = paginator.num_pages

        previous = None if not data.has_previous() else data.previous_page_number()
        next = None if not data.has_next() else data.next_page_number()
        serializer = ProductListSerializer(data, many=True)
        self.page_data = {'count': count, 'pages': pages, 'previous': previous, 'next': next, 'data': serializer.data}


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
    query = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    categories = serializers.ListField(child=serializers.IntegerField(required=False), required=False)
    brands = serializers.ListField(child=serializers.IntegerField(required=False), required=False)
    sizes = serializers.ListField(child=serializers.IntegerField(required=False), required=False)
    paging = PagingSerializer(required=True)

    class Meta:
        fields = [
            'query',
        ]

    def __repr__(self):
        return f"<ProductSearchRequest query:{self.query},Category:{self.categories}, Brand:{self.brands}, Size:{self.sizes}>"


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


class SimilarProductsRequestSerializer(serializers.Serializer):
    categoryIds = serializers.ListField(child=serializers.IntegerField())
    limit = serializers.IntegerField()


class SimilarProductsResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='product.id', read_only=True)
    sku = serializers.CharField(source='product.sku', read_only=True)
    title = serializers.CharField(source='product.title', read_only=True)
    price = serializers.FloatField(source='product.price', read_only=True)
    salePrice = serializers.FloatField(source='product.sale_price', read_only=True)
    uuid = serializers.CharField(source='product.uuid', read_only=True)
    previewImage = ImagesSerializer(source='preview_image', read_only=True)
    averageRating = serializers.FloatField(source='product.average_rating', read_only=True)
    numberOfRatings = serializers.IntegerField(source='product.number_of_ratings', read_only=True)

    class Meta:
        fields = [
            'id',
            'sku',
            'title',
            'price',
            'salePrice',
            'averageRating',
            'numberOfRatings',
            'previewImage'
            'uuid'
        ]


class ProductAttributesSerializer(serializers.Serializer):
    colors = ProductAttributeValuesSerializer(source='colors', read_only=True)
    sizes = ProductAttributeValuesSerializer(source='sizes', read_only=True)
    genders = ProductAttributeValuesSerializer(source='genders', read_only=True)

    class Meta:
        fields = [
            'colors',
            'sizes',
            'genders'
        ]
