import logging

from rest_framework import serializers
from django.core.paginator import Paginator
from .models import Product
from .validators import unique_product_title, validate_sku, product_exists
from auth.serializers import UserPublicSerializer
from comments.serializers import CommentSerializer

logger = logging.getLogger('django')


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[unique_product_title])
    owner = UserPublicSerializer(source='user', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'title',
            'content',
            'owner',
            'price',
            'inventory',
            'sale_price',
            'uuid',
            'comments'
        ]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'title',
            'content',
            'price',
            'inventory',
            'sale_price',
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
    owner = UserPublicSerializer(source='user', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'title',
            'content',
            'owner',
            'price',
            'inventory',
        ]

    def save(self):
        user = self.context.get("logged_in_user")
        sku = self.validated_data['sku']
        title = self.validated_data['title']
        content = self.validated_data['content']
        price = self.validated_data['price']
        inventory = self.validated_data['inventory']
        new_product = Product(sku=sku, user=user, title=title, content=content, price=price, inventory=inventory)
        new_product.save()
        return new_product


class PostProductComment(serializers.Serializer):
    product_id = serializers.IntegerField(validators=[product_exists])
    comment = serializers.CharField()

    def __repr__(self):
        return f"<PostProductComment ProductId:{self.product_id},  Comment:{self.comment}>"


class ProductSearchRequestSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
    category_id = serializers.IntegerField(required=False)
    brand_id = serializers.IntegerField(required=False)
    size_id = serializers.IntegerField(required=False)

    def __repr__(self):
        return f"<ProductSearchRequest query:{self.query},Category:{self.category_id}, Brand:{self.brand_id}, Size:{self.size_id}>"
