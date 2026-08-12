from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile
from tweets.models import Notification


class FollowNotificationTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="otherpass123"
        )

    def test_follow_creates_notification(self):
        self.client.login(
            username="testuser",
            password="testpass123"
        )

        response = self.client.post(
            f"/profile/{self.other_user.username}/follow/"
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.user.profile.following.filter(
                id=self.other_user.id
            ).exists()
        )

        notification = Notification.objects.filter(
            user=self.other_user
        ).first()

        self.assertIsNotNone(notification)

        self.assertEqual(
            notification.message,
            "testuser started following you."
        )