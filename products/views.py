import logging
from rest_framework import serializers
from rest_framework.request import Request

from cfehome.constants.security_constants import ADD_PRODUCT, CHANGE_PRODUCT
from cfehome.decorators.pre_autorize import pre_authorize
from cfehome.utils.security_utils import SecurityUtils
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
def get_product(request: Request, uuid: str, *args, **kwargs):
    product = product_service.find_by_uuid(uuid, True)
    logger.info(f'---> Product Views ---> product: {product}')
    data = ProductSerializer(product, many=False).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_similar_products(request: Request):
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
def get_similar_products_by_uuid(request: Request, uuid: str):
    limit = request.GET.get('limit', 5)
    logger.info(f'---> Product Views ---> limit: {limit}')
    categories = product_service.find_product_categories(uuid)
    category_ids = [category.id for category in categories]
    products = product_service.find_similar_products(category_ids, limit)
    data = SimilarProductsResponseSerializer(products, many=True).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_attributes(request: Request, uuid: str):
    results = product_service.find_product_attributes(uuid)
    data = ProductAttributesSerializer(results).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_images(request: Request, uuid: str):
    images = product_service.find_product_images_by_uuid(uuid)
    data = ImagesSerializer(images, many=True, read_only=True).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_supplier_product(request: Request, uuid: str):
    logged_in_user = request.user
    product = product_service.find_users_product_by_uuid(uuid, logged_in_user)
    data = ProductSerializer(product, many=False).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_products(request: Request):
    queryset = product_service.find_all_products()
    serializer = PaginatedProductListSerializer(queryset, request)
    return Response(serializer.page_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_supplier_products(request: Request):
    logged_in_user = request.user
    queryset = product_service.find_supplier_products(logged_in_user)
    serializer = PaginatedProductListSerializer(queryset, request)
    return Response(serializer.page_data)


def create_page_obj(request: Request, queryset):
    page = request.GET.get('page', 1)
    size = request.GET.get('size', 10)
    logger.info(f'---> Product Views ---> page: {page}')
    logger.info(f'---> Product Views ---> size: {size}')
    paginator = Paginator(queryset, size)
    return paginator.page(page)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@pre_authorize(f"hasPermission({ADD_PRODUCT})")
def create_product(request: Request):
    logged_in_user = SecurityUtils.get_user_from_request(request)
    serializer = SaveProductSerializer(data=request.data)
    images = request.data.getlist("images")
    if serializer.is_valid(raise_exception=True):
        created_product = product_service.create_product(serializer, images, logged_in_user)
        logger.info(f'---> Product Views ---> create_product ---> created_product uuid: {created_product.uuid}')
        return Response({'productId': created_product.uuid}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@pre_authorize(f"hasPermission({CHANGE_PRODUCT}) && securityService.is_product_mine(uuid)")
def update_product(request: Request, uuid: str):
    logged_in_user = SecurityUtils.get_user_from_request(request)
    existing_product = product_service.find_by_uuid(uuid, False)
    if existing_product is None:
        raise serializers.ValidationError({'error.product': "Product does not exist"})
    serializer = UpdateProductSerializer(data=request.data)
    images = request.data.getlist("images")
    if serializer.is_valid(raise_exception=True):
        updated_product = product_service.update_product(existing_product, serializer, images, logged_in_user)
        data = ProductSerializer(updated_product, many=False).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def post_product_comment(request: Request):
    logged_in_user = request.user
    serializer = PostProductComment(data=request.data, many=False)
    if serializer.is_valid(raise_exception=True):
        product = product_service.post_product_comment(serializer, logged_in_user)
        response = ProductSerializer(product, many=False).data
        return Response(response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_products(request: Request):
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
def get_categories_with_totals(request: Request):
    result = product_service.get_categories_with_totals()
    data = CategoriesWithTotalsSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_brands_with_totals(request: Request):
    result = product_service.get_brands_with_totals()
    data = BrandsWithTotalsSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sizes_with_totals(request: Request):
    result = product_service.get_sizes_with_totals()
    data = SizesWithTotalsSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_brands(request: Request):
    result = product_service.find_all_brands()
    data = BrandSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_categories(request: Request):
    result = product_service.find_all_categories()
    data = CategorySerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_attributes(request: Request):
    result = product_service.find_all_attributes()
    data = AllAttributeOptionsSerializer(result).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_sizes(request: Request):
    result = product_service.find_all_sizes()
    data = AttributeOptionSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_colours(request: Request):
    result = product_service.find_all_colours()
    data = AttributeOptionSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_genders(request: Request):
    result = product_service.find_all_genders()
    data = AttributeOptionSerializer(result, many=True).data
    return Response(data, status=status.HTTP_200_OK)

