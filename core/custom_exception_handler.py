import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

# Configure logging
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            response.data = {
                "error": "Authentication credentials were not provided or are invalid.",
                "details": "Ensure you include a valid JWT token in the Authorization header."
            }
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            response.data = {
                "error": "You do not have permission to perform this action.",
                "details": "Check your access rights or contact the administrator."
            }
    else:
        # If no response was created, handle the unhandled exception (e.g., 500 Internal Server Error)
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        response = Response(
            {
                "error": "Internal Server Error",
                "details": "An unexpected error occurred. Please try again later.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
