from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj can be a Message or Conversation instance
        """
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        elif isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        return False
