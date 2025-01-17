import jwt
from django.conf import settings
import logging

logger = logging.getLogger('django')

class SecurityUtils:

    @staticmethod
    def get_token_from_request(request):
        return request.auth

    @staticmethod
    def get_claims_from_request(request):
        token = SecurityUtils.get_token_from_request(request)
        decoded_jwt = jwt.decode(str(token), settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_jwt

    @staticmethod
    def get_user_from_request(request):
        logged_in_user = request.user
        logger.info(f'---> Product Views ---> logged_in_user: {logged_in_user}')
        return logged_in_user