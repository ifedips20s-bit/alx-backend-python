from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and sending messages.
    Only participants of a conversation can view or send messages.
    Supports filtering by conversation_id and pagination.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        """
        Return messages only for conversations where the current user is a participant.
        Optionally filter by conversation_id using query params.
        """
        queryset = Message.objects.filter(conversation__participants=self.request.user)
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        return queryset
def create(self, request, *args, **kwargs):
        """
        Override create to ensure user is a participant in the conversation
        before sending a message.
        """
        conversation_id = request.data.get("conversation_id")
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You do not have permission to send messages to this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Attach conversation instance before saving
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(conversation=conversation, sender=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)