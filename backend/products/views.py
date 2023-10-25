from .serializers import ProductSerializer
from .models import Product
from rest_framework import generics, mixins, permissions,authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from auth.mixins import StaffEditorPermissionMixin, UserQuerySetMixin


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


@api_view(['GET'])
def get_product(request, pk=None, *args, **kwargs):
    obj = get_object_or_404(Product, pk=pk)
    data = ProductSerializer(obj, many=False).data
    return Response(data)

