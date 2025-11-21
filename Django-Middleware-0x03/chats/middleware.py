from datetime import datetime
from django.http import HttpResponseForbidden
import logging

# Use the same logger as your RequestLoggingMiddleware
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    """
    Middleware to log every request to requests.log
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        now = datetime.now()
        log_message = f"{now} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict chat access outside 9AM - 6PM server time.
    Logs every attempt.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        now = datetime.now()
        current_time = now.time()
        start_time = datetime.strptime("09:00", "%H:%M").time()
        end_time = datetime.strptime("18:00", "%H:%M").time()

        # Log every access attempt
        log_message = f"{now} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        # Restrict chat endpoints
        if request.path.startswith("/api/chats/") or request.path.startswith("/chats/"):
            if not (start_time <= current_time <= end_time):
                logger.info(f"{now} - Access denied for user: {user}")
                return HttpResponseForbidden("Chat access is allowed only between 9AM and 6PM.")

        response = self.get_response(request)
        return response
