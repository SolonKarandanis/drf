import logging

from images.serializers import ImagesSerializer
from .serializers import ProductSerializer, CreateProductSerializer, PaginatedProductListSerializer, \
    PostProductComment, ProductSearchRequestSerializer, CategoriesWithTotalsSerializer, BrandsWithTotalsSerializer, \
    SizesWithTotalsSerializer, PaginatedPOSTProductListSerializer
from .models import Product
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage
from .product_service import ProductService

product_service = ProductService()

logger = logging.getLogger('django')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request, uuid: str, *args, **kwargs):
    product = product_service.find_by_uuid(uuid)
    data = ProductSerializer(product, many=False).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_images(request, uuid: str):
    images = product_service.find_product_images_by_uuid(uuid)
    data = ImagesSerializer(many=True, read_only=True)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_supplier_product(request, uuid: str):
    logged_in_user = request.user
    product = product_service.find_users_product_by_uuid(uuid, logged_in_user)
    data = ProductSerializer(product, many=False).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_products(request):
    queryset = product_service.find_all_products()
    serializer = PaginatedProductListSerializer(queryset, request)
    return Response(serializer.page_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_supplier_products(request):
    logged_in_user = request.user
    queryset = product_service.find_supplier_products(logged_in_user)
    serializer = PaginatedProductListSerializer(queryset, request)
    return Response(serializer.page_data)


def create_page_obj(request, queryset):
    page = request.GET.get('page', 1)
    size = request.GET.get('size', 10)
    logger.info(f'page: {page}')
    logger.info(f'size: {size}')
    paginator = Paginator(queryset, size)
    return paginator.page(page)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    logged_in_user = request.user
    serializer = CreateProductSerializer(data=request.data, context={'logged_in_user': logged_in_user})
    if serializer.is_valid(raise_exception=True):
        # serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def post_product_comment(request):
    logged_in_user = request.user
    serializer = PostProductComment(data=request.data, many=False)
    if serializer.is_valid(raise_exception=True):
        product = product_service.post_product_comment(serializer, logged_in_user)
        response = ProductSerializer(product, many=False).data
        return Response(response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_products(request):
    logged_in_user = get_user_from_request(request)
    search_request = ProductSearchRequestSerializer(data=request.data)
    if search_request.is_valid(raise_exception=True):
        serialized_data = search_request.data
        products = product_service.search_products(search_request)
        paging = serialized_data["paging"]
        result = PaginatedPOSTProductListSerializer(products, paging)
        return Response(result.page_data)
    return Response(search_request.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories_with_totals(request):
    result = product_service.get_categories_with_totals()
    data = CategoriesWithTotalsSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_brands_with_totals(request):
    result = product_service.get_brands_with_totals()
    data = BrandsWithTotalsSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sizes_with_totals(request):
    result = product_service.get_sizes_with_totals()
    data = SizesWithTotalsSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


def get_user_from_request(request):
    logged_in_user = request.user
    logger.info(f'----->logged_in_user: {logged_in_user}')
    return logged_in_user
