from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from socials.serializers import SocialUserSerializer
from socials.social_service import SocialService

social_service = SocialService()


# Create your views here.
@api_view(['GET'])
def find_users_socials(request):
    user_id = request.GET.get('userId')
    if user_id is None:
        return Response({"userId": "Required"}, status=status.HTTP_400_BAD_REQUEST)
    queryset = social_service.find_users_socials(user_id)
    data = SocialUserSerializer(queryset).data
    return Response(data)
