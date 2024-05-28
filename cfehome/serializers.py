import logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import serializers, pagination

logger = logging.getLogger('django')


class PagingSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=True)
    limit = serializers.IntegerField(required=True)
    sortField = serializers.CharField(required=False)
    sortOrder = serializers.CharField(required=False)





class ModelPaginationSerializer:
    """
    Serializes page objects of querysets.
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

        self.page_data = {'count': count, 'previous': previous, 'next': next}


