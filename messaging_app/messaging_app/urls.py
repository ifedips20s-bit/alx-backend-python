from django.urls import path, include
from rest_framework.routers import DefaultRouter
from messaging_app.chats.views import MessageViewSet
from messaging_app.chats import auth as chats_auth

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(chats_auth.urlpatterns)),  # JWT token endpoints
]
