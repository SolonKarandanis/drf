import logging
from typing import List

from cfehome.constants.security_constants import ADD_PRODUCT
from cfehome.utils.security_utils import SecurityUtils
from cfehome.utils.user_util import UserUtil
from images.serializers import ImagesSerializer
from .serializers import ProductSerializer, SaveProductSerializer, PaginatedProductListSerializer, \
    PostProductComment, ProductSearchRequestSerializer, CategoriesWithTotalsSerializer, BrandsWithTotalsSerializer, \
    SizesWithTotalsSerializer, PaginatedPOSTProductListSerializer, SimilarProductsRequestSerializer, \
    SimilarProductsResponseSerializer, BrandSerializer, CategorySerializer, AttributeOptionSerializer, \
    ProductAttributesSerializer, AllAttributeOptionsSerializer, UpdateProductSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from .product_service import ProductService

product_service = ProductService()

logger = logging.getLogger('django')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request, uuid: str, *args, **kwargs):
    product = product_service.find_by_uuid(uuid)
    logger.info(f'---> Product Views ---> product: {product}')
    data = ProductSerializer(product, many=False).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_similar_products(request):
    serializer = SimilarProductsRequestSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serialized_data = request.data
        data_dict = dict(serialized_data)
        category_ids = data_dict['categoryIds']
        limit = data_dict['limit']
        products = product_service.find_similar_products(category_ids, limit)
        data = SimilarProductsResponseSerializer(products, many=True).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_similar_products_by_uuid(request, uuid: str):
    limit = request.GET.get('limit', 5)
    logger.info(f'---> Product Views ---> limit: {limit}')
    categories = product_service.find_product_categories(uuid)
    category_ids = [category.id for category in categories]
    products = product_service.find_similar_products(category_ids, limit)
    data = SimilarProductsResponseSerializer(products, many=True).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_attributes(request, uuid: str):
    results = product_service.find_product_attributes(uuid)
    data = ProductAttributesSerializer(results).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_images(request, uuid: str):
    images = product_service.find_product_images_by_uuid(uuid)
    data = ImagesSerializer(images, many=True, read_only=True).data
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
    logger.info(f'---> Product Views ---> page: {page}')
    logger.info(f'---> Product Views ---> size: {size}')
    paginator = Paginator(queryset, size)
    return paginator.page(page)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    logged_in_user = SecurityUtils.get_user_from_request(request)
    can_add_product = SecurityUtils.has_permission(request, ADD_PRODUCT)
    logger.info(f'---> Product Views ---> create_product ---> can_add_product: {can_add_product}')
    serializer = SaveProductSerializer(data=request.data)
    images = request.data.getlist("images")
    if serializer.is_valid(raise_exception=True):
        created_product = product_service.create_product(serializer, images, logged_in_user)
        logger.info(f'---> Product Views ---> create_product ---> created_product uuid: {created_product.uuid}')
        return Response({'productId': created_product.uuid}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, uuid: str):
    logged_in_user = SecurityUtils.get_user_from_request(request)
    is_product_mine = False
    serializer = UpdateProductSerializer(data=request.data)
    images = request.data.getlist("images")
    if serializer.is_valid(raise_exception=True):
        updated_product = product_service.update_product(uuid, serializer, images, logged_in_user)
        data = ProductSerializer(updated_product, many=False).data
        return Response(data)
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
    logged_in_user = SecurityUtils.get_user_from_request(request)
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_brands(request):
    result = product_service.find_all_brands()
    data = BrandSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_categories(request):
    result = product_service.find_all_categories()
    data = CategorySerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_attributes(request):
    result = product_service.find_all_attributes()
    data = AllAttributeOptionsSerializer(result).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_sizes(request):
    result = product_service.find_all_sizes()
    data = AttributeOptionSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_colours(request):
    result = product_service.find_all_colours()
    data = AttributeOptionSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_genders(request):
    result = product_service.find_all_genders()
    data = AttributeOptionSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)

