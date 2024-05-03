from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_logged_in_user_rooms(request):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_rooms(request, uuid):
    pass
