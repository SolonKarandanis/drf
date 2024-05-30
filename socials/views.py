import logging

from rest_framework.response import Response
from rest_framework.decorators import api_view

from socials.serializers import SocialUserSerializer
from socials.social_service import SocialService

social_service = SocialService()

logger = logging.getLogger('django')


# Create your views here.
@api_view(['GET'])
def find_users_socials(request, user_id):
    queryset = social_service.find_users_socials(user_id)
    data = SocialUserSerializer(queryset, many=True).data
    return Response(data)
