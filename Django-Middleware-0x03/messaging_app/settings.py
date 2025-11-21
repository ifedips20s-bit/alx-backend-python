DEBUG = True  # keep True while developing locally
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse
import logging
import time
from collections import defaultdict

# Logger setup
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    """Middleware to log every request"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        now = datetime.now()
        logger.info(f"{now} - User: {user} - Path: {request.path}")
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    """Middleware to restrict chat access outside 9AM-6PM"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        now = datetime.now()
        current_time = now.time()
        start_time = datetime.strptime("09:00", "%H:%M").time()
        end_time = datetime.strptime("18:00", "%H:%M").time()

        logger.info(f"{now} - User: {user} - Path: {request.path}")

        if request.path.startswith("/api/chats/") or request.path.startswith("/chats/"):
            if not (start_time <= current_time <= end_time):
                logger.info(f"{now} - Access denied for user: {user}")
                return HttpResponseForbidden("Chat access is allowed only between 9AM and 6PM.")

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    """Middleware to limit chat messages per IP (5 per minute)"""
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_times = defaultdict(list)
        self.MAX_MESSAGES = 5
        self.TIME_WINDOW = 60

    def __call__(self, request):
        ip = self.get_client_ip(request)

        if request.method == "POST" and (request.path.startswith("/api/chats/") or request.path.startswith("/chats/")):
            now = time.time()
            self.message_times[ip] = [t for t in self.message_times[ip] if now - t < self.TIME_WINDOW]

            if len(self.message_times[ip]) >= self.MAX_MESSAGES:
                return JsonResponse(
                    {"error": "Message limit reached. Try again in a few seconds."}, status=429
                )

            self.message_times[ip].append(now)

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR", "")

class RolePermissionMiddleware:
    """Middleware to check if user has admin/moderator role"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/chats/") or request.path.startswith("/chats/"):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("You must be logged in to access this resource.")

            if getattr(user, "role", "").lower() not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to perform this action.")

        return self.get_response(request)
