# logging_middleware.py
import logging
import traceback
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger('django')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request
        logger.info(f"Request: {request.method} {request.path} from {request.META.get('REMOTE_ADDR')}")
        
        response = self.get_response(request)
        
        # Log response status
        logger.info(f"Response: {response.status_code}")
        
        return response

    def process_exception(self, request, exception):
        logger.error(f"Exception in {request.method} {request.path}: {str(exception)}\n{traceback.format_exc()}")
        return None