import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
logger = logging.getLogger('django')
from .models import Comment


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')