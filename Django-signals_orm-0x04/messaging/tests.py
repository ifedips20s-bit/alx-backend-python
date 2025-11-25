from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import Message, Notification

User = get_user_model()


class MessagingSignalTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="sender", password="1234")
        self.user2 = User.objects.create_user(username="receiver", password="1234")

    def test_notification_created_on_message(self):
        # Create a message
        msg = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello!"
        )

        # Check that one notification exists
        self.assertEqual(Notification.objects.count(), 1)

        notif = Notification.objects.first()
        self.assertEqual(notif.user, self.user2)
        self.assertEqual(notif.message, msg)

