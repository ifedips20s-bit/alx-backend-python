from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer

# ----------------------------
# Conversation ViewSet
# ----------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with the requesting user and optional additional participants.
        """
        participants_ids = request.data.get('participants', [])
        if not isinstance(participants_ids, list):
            return Response({"error": "participants must be a list of user IDs."}, status=status.HTTP_400_BAD_REQUEST)

        # Include the requesting user automatically
        participants_ids.append(str(request.user.user_id))

        participants = User.objects.filter(user_id__in=participants_ids).distinct()
        if not participants.exists():
            return Response({"error": "No valid participants found."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ----------------------------
# Message ViewSet
# ----------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Send a message in an existing conversation.
        """
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body', '').strip()

        if not conversation_id or not message_body:
            return Response({"error": "conversation_id and message_body are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
