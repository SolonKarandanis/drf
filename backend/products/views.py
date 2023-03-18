from .serializers import ProductSerializer
from .models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def get_products(request):
    instance = Product.objects.all().first()
    data = {}
    if instance:
        data = ProductSerializer(instance).data

    return Response(data, headers={"content-type": "application/json"})


@api_view(["POST"])
def save_product(request):
    selializer = ProductSerializer(data=request.data)
    if selializer.is_valid(raise_exception=True):
        instance = selializer.save()
        return Response(selializer.data)
