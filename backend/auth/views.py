import logging
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
def get_all_users(request):
    queryset = User.objects.all()
    data = UserSerializer(queryset, many=True).data
    logger.info(f'data: {data}')
    return Response(data)


@api_view(['POST'])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)
