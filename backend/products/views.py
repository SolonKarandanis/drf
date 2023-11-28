import logging

from .serializers import ProductSerializer, CreateProductSerializer, PaginatedProductListSerializer
from .models import Product
from rest_framework import status
from rest_framework import generics, mixins, permissions, authentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage
from auth.mixins import StaffEditorPermissionMixin, UserQuerySetMixin
from .product_repository import ProductRepository

repo = ProductRepository()

logger = logging.getLogger('django')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request, pk, *args, **kwargs):
    product = repo.find_by_id(pk)
    data = ProductSerializer(product, many=False).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_supplier_product(request, pk):
    logged_in_user = request.user
    product = repo.find_users_product_by_id(pk, logged_in_user)
    data = ProductSerializer(product, many=False).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_products(request):
    queryset = repo.find_all_products()
    serializer = PaginatedProductListSerializer(queryset, request)
    return Response(serializer.page_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_supplier_products(request):
    logged_in_user = request.user
    queryset = repo.find_supplier_products(logged_in_user)
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
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


product_mixin_view = ProductMixinView.as_view()


class ProductListCreateAPIView(generics.ListCreateAPIView, StaffEditorPermissionMixin, UserQuerySetMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication]


product_list_create_view = ProductListCreateAPIView.as_view()


class ProductCreateAPIView(generics.CreateAPIView, StaffEditorPermissionMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)


product_create_view = ProductCreateAPIView.as_view()


class ProductDetailAPIView(generics.RetrieveAPIView, StaffEditorPermissionMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView, StaffEditorPermissionMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title


product_update_view = ProductUpdateAPIView.as_view()


class ProductDeleteAPIView(generics.DestroyAPIView, StaffEditorPermissionMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


product_delete_view = ProductDeleteAPIView.as_view()
