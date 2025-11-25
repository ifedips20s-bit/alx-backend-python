from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Tracks if a message has been edited
    edited = models.BooleanField(default=False)
    
    # Tracks which user last edited the message
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="edited_messages",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"Message {self.id} from {self.sender} to {self.receiver}"


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
