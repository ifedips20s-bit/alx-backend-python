from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse
import logging
import time
from collections import defaultdict

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

class OffensiveLanguageMiddleware:
    """
    Middleware to limit chat messages per IP address.
    Max 5 messages per minute.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track timestamps of messages per IP
        self.message_times = defaultdict(list)
        self.MAX_MESSAGES = 5
        self.TIME_WINDOW = 60  # 60 seconds

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Only track POST requests to chat endpoints
        if request.method == "POST" and (request.path.startswith("/api/chats/") or request.path.startswith("/chats/")):
            now = time.time()
            # Remove timestamps older than TIME_WINDOW
            self.message_times[ip] = [t for t in self.message_times[ip] if now - t < self.TIME_WINDOW]

            if len(self.message_times[ip]) >= self.MAX_MESSAGES:
                return JsonResponse(
                    {"error": "Message limit reached. Try again in a few seconds."}, status=429
                )

            # Add current message timestamp
            self.message_times[ip].append(now)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """Get client IP from request headers"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip