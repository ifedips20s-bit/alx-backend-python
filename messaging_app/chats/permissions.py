from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, send, update, or delete messages.
    """

    # Methods that require object-level permission for modifications
    restricted_methods = ["PUT", "PATCH", "DELETE"]

    def has_permission(self, request, view):
        # Ensure user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj can be a Message or Conversation instance
        """
        if request.method in self.restricted_methods:
            # Only allow modification if user is a participant
            if isinstance(obj, Message):
                return request.user in obj.conversation.participants.all()
            elif isinstance(obj, Conversation):
                return request.user in obj.participants.all()
            return False
        else:
            # Allow any participant to view or create messages
            if isinstance(obj, Message):
                return request.user in obj.conversation.participants.all()
            elif isinstance(obj, Conversation):
                return request.user in obj.participants.all()
            return False
