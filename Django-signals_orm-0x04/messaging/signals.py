from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Logs old content before message is updated.
    """
    if not instance.pk:
        # New message → do nothing
        return

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Only act if content changed
    if old_instance.content != instance.content:
        # Save history of old content
        MessageHistory.objects.create(
            message=old_instance,
            old_content=old_instance.content,
            edited_by=instance.edited_by  # record who made the edit
        )

        # Mark message as edited
        instance.edited = True

from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    Automatically delete messages, notifications, and message history
    when a user is deleted.
    """
    # Delete all messages sent or received by this user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete all notifications for this user
    Notification.objects.filter(user=instance).delete()
    
    # Delete all message histories where this user edited messages
    MessageHistory.objects.filter(edited_by=instance).delete()
