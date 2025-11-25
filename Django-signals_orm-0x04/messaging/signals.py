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
            old_content=old_instance.content
        )

        # Mark message as edited
        instance.edited = True
