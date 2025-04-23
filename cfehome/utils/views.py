from django.http import JsonResponse


def error_404(request, exception):
    message = 'Resource not found'
    return JsonResponse(data={'message': message}, status=404)


def error_500(request, exception):
    message = 'Server Error'
    return JsonResponse(data={'message': message}, status=500)
