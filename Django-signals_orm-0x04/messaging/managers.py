from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to fetch unread messages for a specific user.
    Optimized with .only() to improve performance.
    """

    def unread_for_user(self, user):
        return (
            self.filter(receiver=user, read=False)
            .only("id", "sender", "receiver", "content", "timestamp")
        )
