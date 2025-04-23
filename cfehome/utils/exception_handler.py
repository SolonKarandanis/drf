from rest_framework.views import exception_handler


def custom_exception_handler(exception, context):
    handlers = {
        'ValidationError': _handle_generic_error,
        'Http404': _handle_generic_error,
        'PermissionDenied': _handle_generic_error,
        'NotAuthenticated': _handle_authentication_error,
    }
    response = exception_handler(exception, context)
    exception_class = exception.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exception, context, response)
    return response


def _handle_authentication_error(exception, context, response):
    response.data = {
        'error': 'Please login to proceed'
    }
    return response


def _handle_generic_error(exception, context, response):
    return response
