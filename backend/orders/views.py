from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

import logging
from .models import Order
# Create your views here.
logger = logging.getLogger('django')
