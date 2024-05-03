from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .tasks import send_mail_task


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def send_mail_to_all(request):
    send_mail_task.delay()
    return Response({"Message": "Mail sent"}, status=202)
