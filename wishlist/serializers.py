from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import serializers

from images.serializers import ImagesSerializer
import logging

logger = logging.getLogger('django')


class RemoveWishListItem(serializers.Serializer):
    wishListItemId = serializers.IntegerField(source='wish_list_item_id')

    class Meta:
        fields = [
            'wishListItemId'
        ]


class AddToWishList(serializers.Serializer):
    productId = serializers.IntegerField()
    attributes = serializers.CharField(required=False)

    class Meta:
        fields = [
            'productId',
            'attributes',
        ]

    def __repr__(self):
        return f"<AddToWishlist ProductId:{self.product_id},  attributes:{self.attributes}>"


class WishListItemProductSerializer(serializers.Serializer):
    sku = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    uuid = serializers.CharField(read_only=True)


class WishListItemSerializer(serializers.Serializer):
    uuid = serializers.CharField(source='wish_list_item.uuid', read_only=True)
    attributes = serializers.CharField(source='wish_list_item.attributes', read_only=True)
    previewImage = ImagesSerializer(source='preview_image', read_only=True)
    productDetails = WishListItemProductSerializer(source='product_details', read_only=True)

    class Meta:
        fields = [
            'productDetails',
            'previewImage'
            'uuid',
            'attributes'
        ]


class PaginatedPOSTWishListItemsSerializer:

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
        serializer = WishListItemSerializer(data, many=True)
        self.page_data = {'count': count, 'pages': pages, 'previous': previous, 'next': next, 'data': serializer.data}