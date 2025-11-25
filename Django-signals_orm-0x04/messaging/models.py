from django.db import models
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager

User = get_user_model()


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.filter(receiver=user, read=False).only(
            "id", "sender", "receiver", "content", "timestamp"
        )

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User, null=True, blank=True, related_name="edited_messages", on_delete=models.SET_NULL
    )

    # Self-referential foreign key to allow replies to messages
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE
    )

 # New field to track if the message has been read
    read = models.BooleanField(default=False)

    # Attach the custom manager
    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  # custom manager

    def __str__(self):
        return f"Message {self.id} from {self.sender} to {self.receiver}"

    def get_thread(self):
        """
        Recursively fetch all replies to this message in a threaded format.
        """
        thread = []
        def _fetch_replies(message):
            for reply in message.replies.all():
                thread.append(reply)
                _fetch_replies(reply)
        _fetch_replies(self)
        return thread


class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="notifications", on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name="history", on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="message_histories",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"
