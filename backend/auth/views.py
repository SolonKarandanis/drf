import logging

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer

logger = logging.getLogger('django')


# Create your views here.

@api_view(['GET'])
def get_all_users(request):
    queryset = User.objects.all()
    data = UserSerializer(queryset, many=True).data
    logger.info(f'data: {data}')
    return Response(data)
