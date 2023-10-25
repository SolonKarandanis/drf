import logging
from django.core.paginator import Paginator, EmptyPage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import
from .models import User
from .serializers import UserSerializer, CreateUserSerializer

logger = logging.getLogger('django')


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    page = request.GET.get('page', 1)
    size = request.GET.get('size', 10)
    logger.info(f'page: {page}')
    logger.info(f'size: {size}')
    queryset = User.objects.all()
    paginator = Paginator(queryset, size)
    try:
        page_obj = paginator.page(page)
    except EmptyPage:
        return Response({"invalid": "Page not Found"}, status=status.HTTP_400_BAD_REQUEST)
    data = UserSerializer(page_obj, many=True).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)
